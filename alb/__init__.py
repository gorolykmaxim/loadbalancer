from alb.business import BusinessLayerFacade, BusinessProcessError
from core.config import Config
from alb.integration import IntegrationLayer, ProxyError
from alb.service import ServiceLayer, BAD_REQUEST, INTERNAL_ERROR, GET, POST, DELETE, PUT


class AdvancedLoadbalancer(object):

    def __init__(self):
        self.__config = Config()
        self.__integration_layer = IntegrationLayer(proxy_url=self.__config.get_attribute('proxy_url'))
        self.__business_layer = BusinessLayerFacade(integration_layer=self.__integration_layer)
        self.__service_layer = ServiceLayer(host=self.__config.get_attribute('host'),
                                            port=self.__config.get_attribute('port'))

    def main(self):
        self.__service_layer.map_business_error(BusinessProcessError, BAD_REQUEST)
        self.__service_layer.map_business_error(ProxyError, INTERNAL_ERROR)
        node_groups_url = '/node_group'
        self.__service_layer.map_business_process(method=GET,
                                                  url=node_groups_url,
                                                  business_process=self.__business_layer.get_node_groups)
        node_group_url = '/node_group/{group_name}'
        self.__service_layer.map_business_process(method=GET,
                                                  url=node_group_url,
                                                  business_process=self.__business_layer.get_node_group)
        self.__service_layer.map_business_process(method=POST,
                                                  url=node_group_url,
                                                  business_process=self.__business_layer.create_node_group)
        self.__service_layer.map_business_process(method=DELETE,
                                                  url=node_group_url,
                                                  business_process=self.__business_layer.remove_node_group)
        nodes_url = '/node_group/{group_name}/node'
        self.__service_layer.map_business_process(method=GET,
                                                  url=nodes_url,
                                                  business_process=self.__business_layer.get_nodes)
        node_url = '/node_group/{group_name}/node/{node_name}'
        self.__service_layer.map_business_process(method=GET,
                                                  url=node_url,
                                                  business_process=self.__business_layer.get_node)
        self.__service_layer.map_business_process(method=POST,
                                                  url=node_url,
                                                  business_process=self.__business_layer.create_node)
        self.__service_layer.map_business_process(method=PUT,
                                                  url=node_url,
                                                  business_process=self.__business_layer.update_node)
        self.__service_layer.map_business_process(method=DELETE,
                                                  url=node_url,
                                                  business_process=self.__business_layer.remove_node)
        attributes_url = '/node_group/{group_name}/node/{node_name}/attribute'
        self.__service_layer.map_business_process(method=GET,
                                                  url=attributes_url,
                                                  business_process=self.__business_layer.get_node_attributes)
        attribute_url = '/node_group/{group_name}/node/{node_name}/attribute/{attribute_name}'
        self.__service_layer.map_business_process(method=GET,
                                                  url=attribute_url,
                                                  business_process=self.__business_layer.get_node_attribute)
        self.__service_layer.map_business_process(method=POST,
                                                  url=attribute_url,
                                                  business_process=self.__business_layer.create_node_attribute)
        self.__service_layer.map_business_process(method=PUT,
                                                  url=attribute_url,
                                                  business_process=self.__business_layer.update_node_attribute)
        self.__service_layer.map_business_process(method=DELETE,
                                                  url=attribute_url,
                                                  business_process=self.__business_layer.remove_node_attribute)
        self.__service_layer.run()
