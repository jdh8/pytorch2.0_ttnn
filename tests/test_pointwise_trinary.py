
import torch
import torch_ttnn
import ttnn
import unittest

class TestModules(unittest.TestCase):
    def setUp(self):
        # Open device 0
        self.device: ttnn.Device = ttnn.open_device(device_id=0)

    def tearDown(self):
        # Close the device
        ttnn.close_device(self.device)


    def test_addcdiv(self):
        class AddcdivModule(torch.nn.Module):
            def __init__(self): super().__init__()
            def forward(self, x, y, z): return torch.addcdiv(x, y, z)
            def input_types(self): return [((4, 4), torch.float16), ((4, 4), torch.float16), ((4, 4), torch.float16)]

        m = AddcdivModule()
        input_types = m.input_types()
        inputs = [
            torch.randint(1, 3, type[0]).type(type[1]) for type in input_types
        ]
        result_before = m.forward(*inputs)
        option = torch_ttnn.TenstorrentBackendOption(device=self.device)
        # The compilation is lazy, so we need to run forward once to trigger the compilation
        m = torch.compile(m, backend=torch_ttnn.backend(option))
        result_after = m.forward(*inputs)
        self.assertEqual(1, len(option._out_fx_graphs))
        option._out_fx_graphs[0].print_tabular()

        # Check the graph has be rewritten and contain ttnn ops
        nodes = list(option._out_fx_graphs[0].nodes)
        self.assertEqual(nodes[9].target, ttnn.addcdiv)
        self.assertEqual(nodes[9].args[0].target, ttnn.to_device)
        self.assertEqual(nodes[9].args[0].args[0].target, ttnn.from_torch)
        self.assertEqual(nodes[10].target, ttnn.from_device)
        self.assertEqual(nodes[11].target, ttnn.to_layout)
        self.assertEqual(nodes[12].target, ttnn.to_torch)
        # Check inference result
        self.assertTrue(torch.allclose(result_before, result_after))

    def test_addcmul(self):
        class AddcmulModule(torch.nn.Module):
            def __init__(self): super().__init__()
            def forward(self, x, y, z): return torch.addcmul(x, y, z)
            def input_types(self): return [((4, 4), torch.float16), ((4, 4), torch.float16), ((4, 4), torch.float16)]

        m = AddcmulModule()
        input_types = m.input_types()
        inputs = [
            torch.randint(1, 3, type[0]).type(type[1]) for type in input_types
        ]
        result_before = m.forward(*inputs)
        option = torch_ttnn.TenstorrentBackendOption(device=self.device)
        # The compilation is lazy, so we need to run forward once to trigger the compilation
        m = torch.compile(m, backend=torch_ttnn.backend(option))
        result_after = m.forward(*inputs)
        self.assertEqual(1, len(option._out_fx_graphs))
        option._out_fx_graphs[0].print_tabular()

        # Check the graph has be rewritten and contain ttnn ops
        nodes = list(option._out_fx_graphs[0].nodes)
        self.assertEqual(nodes[9].target, ttnn.addcmul)
        self.assertEqual(nodes[9].args[0].target, ttnn.to_device)
        self.assertEqual(nodes[9].args[0].args[0].target, ttnn.from_torch)
        self.assertEqual(nodes[10].target, ttnn.from_device)
        self.assertEqual(nodes[11].target, ttnn.to_layout)
        self.assertEqual(nodes[12].target, ttnn.to_torch)
        # Check inference result
        self.assertTrue(torch.allclose(result_before, result_after))

    def test_where(self):
        class WhereModule(torch.nn.Module):
            def __init__(self): super().__init__()
            def forward(self, x, y, z): return torch.where(x, y, z)
            def input_types(self): return [((4, 4), torch.bool), ((4, 4), torch.float16), ((4, 4), torch.float16)]

        m = WhereModule()
        input_types = m.input_types()
        inputs = [
            torch.randint(1, 3, type[0]).type(type[1]) for type in input_types
        ]
        result_before = m.forward(*inputs)
        option = torch_ttnn.TenstorrentBackendOption(device=self.device)
        # The compilation is lazy, so we need to run forward once to trigger the compilation
        m = torch.compile(m, backend=torch_ttnn.backend(option))
        result_after = m.forward(*inputs)
        self.assertEqual(1, len(option._out_fx_graphs))
        option._out_fx_graphs[0].print_tabular()

        # Check the graph has be rewritten and contain ttnn ops
        nodes = list(option._out_fx_graphs[0].nodes)
        self.assertEqual(nodes[9].target, ttnn.where)
        self.assertEqual(nodes[9].args[0].target, ttnn.to_device)
        self.assertEqual(nodes[9].args[0].args[0].target, ttnn.from_torch)
        self.assertEqual(nodes[10].target, ttnn.from_device)
        self.assertEqual(nodes[11].target, ttnn.to_layout)
        self.assertEqual(nodes[12].target, ttnn.to_torch)
        # Check inference result
        self.assertTrue(torch.allclose(result_before, result_after))
