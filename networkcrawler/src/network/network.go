package network

import "github.com/aeden/traceroute"

func AnalyzeNetworkChannel(host string) (hops int, latency int, err error) {
	options := traceroute.TracerouteOptions{}
	options.SetMaxHops(30)
	options.SetRetries(1)
	options.SetTimeoutMs(100)
	result, err := traceroute.Traceroute(host, &options)
	if err == nil {
		hops = len(result.Hops)
		if hops > 0 {
			latency = getLatency(result.Hops)
		}
	}
	return hops, latency, err
}

func getLatency(hops []traceroute.TracerouteHop) int {
	lastHop := hops[len(hops)-1]
	return int(lastHop.ElapsedTime.Nanoseconds() / 1000000)
}