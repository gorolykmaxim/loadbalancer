package api

import (
	"fmt"
	"encoding/json"
	"net/http"
	"bytes"
	"io/ioutil"
)

type Attribute struct {
	Value float64 `json:"value"`
	Weight float64 `json:"weight"`
}

type Node struct {
	Host string `json:"host"`
	Port int `json:"port"`
	Weight float64 `json:"weight"`
	Attributes map[string]Attribute `json:"attributes"`
}

type NodeGroup struct {
	Nodes map[string]Node `json:"nodes"`
}

type valueUpdate struct {
	Value int `json:"value"`
}

type valueUpdateError struct {
	code int
}

func (v valueUpdateError) Error() string {
	return fmt.Sprintf("Submission failed with code %d", v.code)
}

// Update value of the latency attribute of the specified node.
func UpdateNodeLatency(apiUrl, group, node string, value int) error {
	return put(apiUrl, group, node, "latency", value)
}

// Update value of the distance attribute of the specified node.
func UpdateNodeDistance(apiUrl, group, node string, value int) error {
	return put(apiUrl, group, node, "distance", value)
}

// Execute a PUT HTTP request. Return an error, if such has occurred.
func put(apiUrl, group, node, attribute string, value int) error {
	url := fmt.Sprintf("%s/node_group/%s/node/%s/attribute/%s", apiUrl, group, node, attribute)
	v, err := json.Marshal(&valueUpdate{value})
	if err != nil {
		return err
	}
	req, err := http.NewRequest("PUT", url, bytes.NewBuffer(v))
	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{}
	response, err := client.Do(req)
	if err == nil {
		defer response.Body.Close()
		if response.StatusCode < 200 || response.StatusCode > 399 {
			return valueUpdateError{code:response.StatusCode}
		}
	}
	return err
}

// Return all node groups. Return an error, if such has occurred.
func GetNodeGroups(apiUrl string) (nodeGroups map[string]NodeGroup, err error){
	url := fmt.Sprintf("%s/node_group", apiUrl)
	response, err := http.Get(url)
	if err != nil {
		return nodeGroups, err
	}
	defer response.Body.Close()
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return nodeGroups, err
	}
	err = json.Unmarshal(body, &nodeGroups)
	return nodeGroups, err
}
