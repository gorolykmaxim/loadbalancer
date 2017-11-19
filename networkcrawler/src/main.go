package main

import (
	"time"
	"os"
	"strconv"
	"fmt"
	"log"
	"api"
	"network"
)

func main() {
	interval, apiUrl := loadConfig()
	for {
		time.Sleep(time.Duration(interval) * time.Second)
		log.Println("Trying to load node groups...")
		nodeGroups, err := api.GetNodeGroups(apiUrl)
		if err != nil {
			template := "Failed to load node groups - %s"
			message := fmt.Sprintf(template, err)
			log.Println(message)
			continue
		}
		log.Println("Successfully loaded node groups!")
		for groupName, group := range nodeGroups {
			for nodeName, node := range group.Nodes {
				go processNode(apiUrl, groupName, nodeName, node)
			}
		}
	}
}

func loadConfig() (int, string) {
	interval := 10
	if v := os.Getenv("INTERVAL") ; v != "" {
		interval, _ = strconv.Atoi(v)
	}
	apiUrl := "http://localhost:5000"
	if v := os.Getenv("API_URL") ; v != "" {
		apiUrl = v
	}
	return interval, apiUrl
}

func processNode(apiUrl, groupName, nodeName string, node api.Node) {
	_, latencyOk := node.Attributes["latency"]
	_, distanceOk := node.Attributes["distance"]
	if latencyOk || distanceOk {
		template := "Analyzing status of the network channel to node '%s' from group '%s'..."
		message := fmt.Sprintf(template, nodeName, groupName)
		log.Println(message)
		hops, latency, err := network.AnalyzeNetworkChannel(node.Host)
		if err != nil {
			template := "Cannot analyze network status of node '%s' from group '%s' - %s"
			message := fmt.Sprintf(template, nodeName, groupName, err)
			log.Println(message)
			return
		}
		if latencyOk {
			template := "Submitting latency of the node '%s' from group '%s'."
			message := fmt.Sprintf(template, nodeName, groupName)
			log.Println(message)
			if err := api.UpdateNodeLatency(apiUrl, groupName, nodeName, latency) ; err != nil {
				template := "Cannot submit latency of node '%s' from group '%s' - %s"
				message := fmt.Sprintf(template, nodeName, groupName, err)
				log.Println(message)
			}
		}
		if distanceOk {
			template := "Submitting distance to the node '%s' from group '%s'."
			message := fmt.Sprintf(template, nodeName, groupName)
			log.Println(message)
			if err := api.UpdateNodeDistance(apiUrl, groupName, nodeName, hops) ; err != nil {
				template := "Cannot submit distance to node '%s' from group '%s' - %s"
				message := fmt.Sprintf(template, nodeName, groupName, err)
				log.Println(message)
			}
		}
	}
}
