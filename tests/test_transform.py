import unittest

from subgrounds.query import Query, Selection
from subgrounds.schema import FieldMeta, TypeRef
from subgrounds.transform import transform_data, transform_selection

class TestQueryTransform(unittest.TestCase):
  def test_transform_selection1(self):
    expected = Query([
      Selection('swaps', None, None, [
        Selection('amount0In', None, None, None),
        Selection('amount0Out', None, None, None),
        Selection('amount1In', None, None, None),
        Selection('amount1Out', None, None, None),
      ])
    ])

    fmeta = FieldMeta('price1', '', [], TypeRef.non_null('Float'))

    query = Query([
      Selection('swaps', None, None, [
        Selection('price1', None, None, None),
      ])
    ])

    replacement = [
      Selection('amount0In', None, None, None),
      Selection('amount0Out', None, None, None),
      Selection('amount1In', None, None, None),
      Selection('amount1Out', None, None, None),
    ]

    new_query = transform_selection(fmeta, replacement, query)

    self.assertEqual(new_query, expected)

  def test_transform_data1(self):
    expected = {
      'price1': 0.5,
      'amount0In': 0.0,
      'amount0Out': 10.0,
      'amount1In': 20.0,
      'amount1Out': 0.0
    }

    data = {
      'amount0In': 0.0,
      'amount0Out': 10.0,
      'amount1In': 20.0,
      'amount1Out': 0.0
    }

    fmeta = FieldMeta('price1', '', [], TypeRef.non_null('Float'))

    def f(in0, out0, in1, out1):
      return abs(in0 - out0) / abs(in1 - out1)

    arg_select = [
      Selection('amount0In', None, None, None),
      Selection('amount0Out', None, None, None),
      Selection('amount1In', None, None, None),
      Selection('amount1Out', None, None, None),
    ]

    query = Query([
      Selection('price1', None, None, None),
    ])

    transformed_data = transform_data(fmeta, f, arg_select, query, data)

    self.assertEqual(transformed_data, expected)

  def test_transform_data2(self):
    expected = {
      'swap': {
        'price1': 0.5,
        'amount0In': 0.0,
        'amount0Out': 10.0,
        'amount1In': 20.0,
        'amount1Out': 0.0
      }
    }

    data = {
      'swap': {
        'amount0In': 0.0,
        'amount0Out': 10.0,
        'amount1In': 20.0,
        'amount1Out': 0.0
      }
    }

    fmeta = FieldMeta('price1', '', [], TypeRef.non_null('Float'))

    def f(in0, out0, in1, out1):
      return abs(in0 - out0) / abs(in1 - out1)

    arg_select = [
      Selection('amount0In', None, None, None),
      Selection('amount0Out', None, None, None),
      Selection('amount1In', None, None, None),
      Selection('amount1Out', None, None, None),
    ]

    query = Query([
      Selection('swap', None, None, [
        Selection('price1', None, None, None),
      ])
    ])

    transformed_data = transform_data(fmeta, f, arg_select, query, data)

    self.assertEqual(transformed_data, expected)

  def test_transform_data3(self):
    expected = {
      'swaps': [{
        'price1': 0.5,
        'amount0In': 0.0,
        'amount0Out': 10.0,
        'amount1In': 20.0,
        'amount1Out': 0.0
      }]
    }

    data = {
      'swaps': [{
        'amount0In': 0.0,
        'amount0Out': 10.0,
        'amount1In': 20.0,
        'amount1Out': 0.0
      }]
    }

    def f(in0, out0, in1, out1):
      return abs(in0 - out0) / abs(in1 - out1)

    arg_select = [
      Selection('amount0In', None, None, None),
      Selection('amount0Out', None, None, None),
      Selection('amount1In', None, None, None),
      Selection('amount1Out', None, None, None),
    ]

    fmeta = FieldMeta('price1', '', [], TypeRef.non_null('Float'))

    query = Query([
      Selection('swaps', None, None, [
        Selection('price1', None, None, None),
      ])
    ])

    transformed_data = transform_data(fmeta, f, arg_select, query, data)

    self.assertEqual(transformed_data, expected)