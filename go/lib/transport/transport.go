package transport

import (
	"net/http"
)

// Transport is a custom transport for Element43 which simply sets the user agent
type Transport struct {
	userAgent string
}

// NewTransport generates a new custom transport
func NewTransport(userAgent string) *Transport {
	return &Transport{
		userAgent: userAgent,
	}
}

// RoundTrip automatically sets the user agent
func (transport *Transport) RoundTrip(request *http.Request) (*http.Response, error) {
	request.Header.Set("User-Agent", transport.userAgent)

	response, err := http.DefaultTransport.RoundTrip(request)

	return response, err
}
