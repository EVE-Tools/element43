package transport

import (
	"errors"
	"net/http"
	"strconv"
	"sync"
	"time"

	"github.com/sirupsen/logrus"
	"golang.org/x/sync/semaphore"
)

// ESITransport is a custom transport for rate-limiting requests to ESI
type ESITransport struct {
	userAgent    string
	timeout      time.Duration
	blockedUntil time.Time
	mutex        sync.RWMutex
	limiter      *semaphore.Weighted
}

// NewESITransport generates a new custom transport
func NewESITransport(userAgent string, timeout time.Duration, concurrencyLimit int64) *ESITransport {
	return &ESITransport{
		userAgent:    userAgent,
		timeout:      timeout,
		blockedUntil: time.Now(),
		limiter:      semaphore.NewWeighted(concurrencyLimit),
	}
}

// RoundTrip uses a default transport which blocks when the client is being blocked by ESI or we're close to the limit.
// Waiting requests will pile-up! Having backpressure in place should be considered.
func (transport *ESITransport) RoundTrip(request *http.Request) (*http.Response, error) {
	transport.mutex.RLock()
	unlockTime := transport.blockedUntil
	timeoutTime := time.Now().Add(transport.timeout)
	transport.mutex.RUnlock()

	if unlockTime.After(time.Now()) {
		// Check if sleeping would exceed timeout, if yes, cancel instantly
		if unlockTime.After(timeoutTime) {
			return nil, errors.New("skipped request, delay would exceed timeout")
		}

		// Sleep until unblock if we're blocked by ESI
		time.Sleep(unlockTime.Sub(time.Now()))
	}

	request.Header.Set("User-Agent", transport.userAgent)

	transport.limiter.Acquire(request.Context(), 1)
	response, err := http.DefaultTransport.RoundTrip(request)
	transport.limiter.Release(1)

	if err != nil {
		return response, err
	}

	if response != nil {
		// Try to parse the remaining errors header
		remainingErrors, err := strconv.ParseInt(response.Header.Get("X-ESI-Error-Limit-Remain"), 10, 64)
		if err != nil {
			// Set to default value above limit
			remainingErrors = 100
		}

		// We're blocked or at least close, defer/skip requests until reset of error window
		if remainingErrors <= 10 || response.StatusCode == 420 || response.Header.Get("X-ESI-Error-Limited") != "" {
			reset := response.Header.Get("X-ESI-Error-Limit-Reset")

			logrus.WithField("reset_in", reset).Warn("Too many errors when calling ESI, waiting until error window resets!")

			if reset != "" {
				windowEndsInSeconds, err := strconv.ParseInt(reset, 10, 64)
				if err != nil {
					return response, err
				}

				transport.mutex.Lock()
				transport.blockedUntil = time.Now().Add(time.Duration(windowEndsInSeconds * 1e9))
				transport.mutex.Unlock()
			}
		}
	}

	return response, err
}
