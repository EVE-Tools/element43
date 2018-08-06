package transport

import (
	"bufio"
	"bytes"
	"compress/gzip"
	"net/http"
	"net/http/httputil"
	"time"

	"github.com/go-redis/redis"
)

// CachingTransport is a redis-based caching wrapper around the custom rate-limited ESITransport
type CachingTransport struct {
	esiTransport *ESITransport
	redisClient  *redis.Client
}

// NewCachingTransport generates a new custom transport
func NewCachingTransport(esiTransport *ESITransport, redisClient *redis.Client) *CachingTransport {
	return &CachingTransport{
		esiTransport: esiTransport,
		redisClient:  redisClient,
	}
}

// RoundTrip tries to fetch the request from cache, otherwise it is fetched via ESITransport
func (transport *CachingTransport) RoundTrip(request *http.Request) (*http.Response, error) {
	// Only cache GET/HEAD
	if request.Method == "GET" || request.Method == "HEAD" {
		// Try to find hot entry in cache
		cacheEntry, err := transport.redisClient.Get(request.URL.String()).Result()
		if err == redis.Nil {
			return transport.executeAndStore(request)
		} else if err != nil {
			panic(err)
		}

		// Show uncompressed response from cache
		reader, err := gzip.NewReader(bytes.NewReader([]byte(cacheEntry)))
		if err != nil {
			panic(err)
		}
		defer reader.Close()

		return http.ReadResponse(bufio.NewReader(reader), request)
	}

	return transport.esiTransport.RoundTrip(request)
}

func (transport *CachingTransport) executeAndStore(request *http.Request) (*http.Response, error) {
	// Make request using the esiTransport
	response, err := transport.esiTransport.RoundTrip(request)
	if err != nil {
		return nil, err
	}

	// Dump copy of request for storage
	dump, err := httputil.DumpResponse(response, true)
	if err != nil {
		panic(err)
	}

	// Asynchronously store contents in cache
	go func(transport *CachingTransport, url string, dump []byte) {
		// Only cache successful responses
		if response.StatusCode == 200 {
			// Parse expiry time for auto-expiry in redis
			expiry, err := time.Parse(time.RFC1123, response.Header.Get("expires"))
			if err != nil {
				panic(err)
			}
			expiryDuration := expiry.Sub(time.Now())

			// Compress response to save some memory
			var compressionBuffer bytes.Buffer
			writer := gzip.NewWriter(&compressionBuffer)
			if _, err = writer.Write(dump); err != nil {
				panic(err)
			}
			if err = writer.Close(); err != nil {
				panic(err)
			}

			// Put data into redis
			_, err = transport.redisClient.Set(request.URL.String(), compressionBuffer.Bytes(), expiryDuration).Result()
			if err != nil {
				panic(err)
			}
		}
	}(transport, request.URL.String(), dump)

	// Return response
	return response, err
}
