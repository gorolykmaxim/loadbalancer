package network

import "C"

import (
	"github.com/aeden/traceroute"
)

//export analyze_network_channel
func analyze_network_channel(host string) (hops int, latency int) {
	options := traceroute.TracerouteOptions{}
	result, err := traceroute.Traceroute(host, &options)
	if err == nil {
		hops = len(result.Hops)
		latency = getLatency(result.Hops)
	}
	return hops, latency
}

func getLatency(hops []traceroute.TracerouteHop) int {
	lastHop := hops[len(hops)-1]
	return int(lastHop.ElapsedTime.Nanoseconds() / 1000000)
}

func main() {
}
