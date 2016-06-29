# -*- coding: utf-8 -*-
import requests


class Spree(object):

    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers['X-Spree-Token'] = api_key

    @property
    def product(self):
        return Product(connection=self)

    @property
    def orders(self):
        return Orders(connection=self)

    @property
    def stock_items(self):
        return StockItems(connection=self)


class Pagination(object):
    def __init__(self, data, items_attribute):
        self.data = data
        self.items = data[items_attribute]
        self.current_index = -1

    @property
    def count(self):
        return self.data['count']

    def __iter__(self):
        return self

    def __getitem__(self, key):
        return self.data

    def next(self):
        self.current_index += 1
        return self.items[self.current_index]


class Resource(object):
    """
    A base class for all Resources to extend
    """

    def __init__(self, connection):
        self.connection = connection

    @property
    def url(self):
        return self.connection.url + self.path

    def load_payload(self, data):
        return data

    def all(self):
        return Pagination(
            self.connection.session.get(self.url).json(),
            self.path[1:]
        )

    def find(self, id):
        "find a given record"
        # str() - ordernumber is a string
        path = self.url + '/%s' % str(id)
        return self.connection.session.get(path).json()

    def create(self, data):
        "create a record with the given data"
        payload = self.load_payload(data)
        return self.connection.session.post(self.url, data=payload).json()

    def update(self, id, data):
        "update the record with given data"
        path = self.url + '/%d' % id
        payload = self.load_payload(data)
        return self.connection.session.put(path, data=payload).json()

    def delete(self, id):
        "delete a given record"
        path = self.url + '/%d' % id
        return self.connection.session.delete(path).json()


class Product(Resource):
    path = '/products'

    def load_payload(self, data):
        payload = {
                'product[name]': data['name']
            }
        if 'price' in data:
            payload['product[price]'] = data['price']
        if 'shipping_category_id' in data:
            payload['product[shipping_category_id]'] = \
                data['shipping_category_id']
        if 'sku' in data:
            payload['product[sku]'] = data['sku']
        if 'description' in data:
            payload['product[description]'] = data['description']
        if 'display_price' in data:
            payload['product[display_price]'] = data['display_price']
        if 'available_on' in data:
            payload['product[available_on]'] = data['available_on']
        if 'meta_description' in data:
            payload['product[meta_description]'] = data['meta_description']
        if 'meta_keywords' in data:
            payload['product[meta_keywords]'] = data['meta_keywords']
        if 'weight' in data:
            payload['product[weight]'] = data['weight']
        if 'height' in data:
            payload['product[height]'] = data['height']
        if 'width' in data:
            payload['product[width]'] = data['width']
        if 'depth' in data:
            payload['product[depth]'] = data['depth']
        if 'cost_price' in data:
            payload['product[cost_price]'] = data['cost_price']

        return super(Product, self).load_payload(payload)


class Orders(Resource):
    path = '/orders'


class StockItems(Resource):
    # TODO
    path = '/stock_locations'
