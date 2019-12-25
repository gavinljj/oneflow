import unittest
import numpy as np

import oneflow as flow

config = flow.function_config()

def make_job(input_shape, axis, dtype=flow.float32):
    config.use_xla_jit(False)
    config.use_tensorrt(False)

    @flow.function(config)
    def softmax_job(x = flow.input_blob_def(input_shape, dtype=dtype)):
        return flow.nn.softmax(x, axis=axis)
    return softmax_job

def make_xla_job(input_shape, axis, dtype=flow.float32):
    config.use_xla_jit(True)
    config.use_tensorrt(False)

    @flow.function(config)
    def xla_softmax_job(x = flow.input_blob_def(input_shape, dtype=dtype)):
        return flow.nn.softmax(x, axis=axis)
    return xla_softmax_job

def make_trt_job(input_shape, axis, dtype=flow.float32):
    config.use_xla_jit(False)
    config.use_tensorrt(True)

    @flow.function(config)
    def trt_softmax_job(x = flow.input_blob_def(input_shape, dtype=dtype)):
        return flow.nn.softmax(x, axis=axis)
    return trt_softmax_job

class TestSoftmax(unittest.TestCase):
    def _test_body(self, x, axis, dtype=np.float32):
        f1 = make_job(x.shape, axis, dtype=flow.float32)
        f2 = make_xla_job(x.shape, axis, dtype=flow.float32)
        a = f1(x).get()
        b = f2(x).get()
        print("without xla: ", a)
        print("with xla: ", b)
        self.assertTrue(np.allclose(a, b , rtol=1e-03, atol=1e-05))
        flow.clear_default_session()

        f3 = make_trt_job(x.shape, axis, dtype=flow.float32)
        c = f3(x).get()
        print("with tensorrt: ", c)
        self.assertTrue(np.allclose(a, c , rtol=1e-03, atol=1e-05))
        flow.clear_default_session()

    def _test_ones_body(self, shape, axis, dtype=np.float32):
        x = np.ones(shape, dtype=dtype)
        self._test_body(x, axis, dtype=dtype)

    def _test_random_body(self, shape, axis, dtype=np.float32):
        x = np.random.random(shape).astype(dtype)
        self._test_body(x, axis, dtype=dtype)

    def test_ones_input(self):
        self._test_ones_body((2, 5), axis=1)
        self._test_ones_body((2, 5), axis=-1)
        self._test_ones_body((1, 5, 2), axis=1)
        self._test_ones_body((1, 5, 2), axis=2)

    def test_random_input(self):
        self._test_random_body((2, 5), axis=1)
        self._test_random_body((2, 5), axis=-1)
        self._test_random_body((1, 5, 2), axis=1)
        self._test_random_body((1, 5, 2), axis=2)

if __name__ == '__main__':
    unittest.main()