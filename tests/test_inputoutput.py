import unittest
import random
import io
import pyrtl
import six
from pyrtl import inputoutput
from pyrtl import analysis


full_adder_blif = """\
# Generated by Yosys 0.3.0+ (git sha1 7e758d5, clang 3.4-1ubuntu3 -fPIC -Os)
.model full_adder
.inputs x y cin
.outputs sum cout
.names $false
.names $true
1
.names y $not$FA.v:12$3_Y
0 1
.names x $not$FA.v:11$1_Y
0 1
.names cin $not$FA.v:15$6_Y
0 1
.names ind3 ind4 sum
1- 1
-1 1
.names $not$FA.v:15$6_Y ind2 ind3
11 1
.names x $not$FA.v:12$3_Y ind1
11 1
.names ind2 $not$FA.v:16$8_Y
0 1
.names cin $not$FA.v:16$8_Y ind4
11 1
.names x y $and$FA.v:19$11_Y
11 1
.names ind0 ind1 ind2
1- 1
-1 1
.names cin ind2 $and$FA.v:19$12_Y
11 1
.names $and$FA.v:19$11_Y $and$FA.v:19$12_Y cout
1- 1
-1 1
.names $not$FA.v:11$1_Y y ind0
11 1
.end
"""

state_machine_blif = """\
# Generated by Yosys 0.5+     420 (git sha1 1d62f87, clang 7.0.2 -fPIC -Os)

.model statem
.inputs clk in reset
.outputs out[0] out[1] out[2] out[3]
.names $false
.names $true
1
.names $undef
.names in state[2] $abc$129$n11_1
11 1
.names $abc$129$n11_1 state[3] $auto$fsm_map.cc:238:map_fsm$30[0]
1- 1
-1 1
.names state[2] $abc$129$n13
0 1
.names state[0] $abc$129$n14_1
0 1
.names state[2] state[1] $abc$129$n15
00 1
.names $abc$129$n15 $abc$129$n14_1 $abc$129$n13 out[0]
-00 1
0-0 1
.names state[1] $abc$129$n17
0 1
.names $abc$129$n15 $abc$129$n14_1 $abc$129$n17 out[1]
-00 1
0-0 1
.names $abc$129$n15 $abc$129$n14_1 out[2]
11 1
.names in $abc$129$n13 $auto$fsm_map.cc:118:implement_pattern_cache$38
00 1
# .subckt $_DFF_PP1_ C=clk D=$auto$fsm_map.cc:238:map_fsm$30[0] Q=state[0] R=reset
# .subckt $_DFF_PP0_ C=clk D=$auto$fsm_map.cc:118:implement_pattern_cache$38 Q=state[1] R=reset
# .subckt $_DFF_PP0_ C=clk D=state[0] Q=state[2] R=reset
# .subckt $_DFF_PP0_ C=clk D=state[1] Q=state[3] R=reset
.names $false out[3]
1 1
.end
"""

# Manually set the .latch's init values from 2 to arbitrary non-1 numbers, for testing.
# Should result in the same logic, but allows for testing the parser.
counter4bit_blif = """\
# Generated by Yosys 0.9 (git sha1 UNKNOWN, clang 11.0.0 -fPIC -Os)

.model counter
.inputs clk rst en
.outputs count[0] count[1] count[2] count[3]
.names $false
.names $true
1
.names $undef
.names count[0] $add$counter.v:10$2_Y[0] en $procmux$3_Y[0]
1-0 1
-11 1
.names count[1] $add$counter.v:10$2_Y[1] en $procmux$3_Y[1]
1-0 1
-11 1
.names count[2] $add$counter.v:10$2_Y[2] en $procmux$3_Y[2]
1-0 1
-11 1
.names count[3] $add$counter.v:10$2_Y[3] en $procmux$3_Y[3]
1-0 1
-11 1
.names $procmux$3_Y[0] $false rst $0\count[3:0][0]
1-0 1
-11 1
.names $procmux$3_Y[1] $false rst $0\count[3:0][1]
1-0 1
-11 1
.names $procmux$3_Y[2] $false rst $0\count[3:0][2]
1-0 1
-11 1
.names $procmux$3_Y[3] $false rst $0\count[3:0][3]
1-0 1
-11 1
.latch $0\count[3:0][0] count[0] re clk 2
.latch $0\count[3:0][1] count[1] re clk 0
.latch $0\count[3:0][2] count[2] re clk 3
.latch $0\count[3:0][3] count[3] re clk
.names count[1] count[0] $techmap$add$counter.v:10$2.$auto$alumacc.cc:474:replace_alu$53.lcu.g[1]
11 1
.names count[2] $techmap$add$counter.v:10$2.$auto$alumacc.cc:474:replace_alu$53.lcu.g[1] $techmap$add$counter.v:10$2.$auto$alumacc.cc:474:replace_alu$53.lcu.g[2]
11 1
.names count[1] count[0] $add$counter.v:10$2_Y[1]
10 1
01 1
.names count[2] $techmap$add$counter.v:10$2.$auto$alumacc.cc:474:replace_alu$53.lcu.g[1] $add$counter.v:10$2_Y[2]
10 1
01 1
.names count[3] $techmap$add$counter.v:10$2.$auto$alumacc.cc:474:replace_alu$53.lcu.g[2] $add$counter.v:10$2_Y[3]
10 1
01 1
.names count[0] $true $add$counter.v:10$2_Y[0]
10 1
01 1
.names count[0] $techmap$add$counter.v:10$2.$auto$alumacc.cc:474:replace_alu$53.lcu.g[0]
1 1
.end
"""  # noqa

counter4bit_blif_bad_latch_inits = """\
# Generated by Yosys 0.9 (git sha1 UNKNOWN, clang 11.0.0 -fPIC -Os)

.model counter
.inputs clk rst en
.outputs count[0] count[1] count[2] count[3]
.names $false
.names $true
1
.names $undef
.names count[0] $add$counter.v:10$2_Y[0] en $procmux$3_Y[0]
1-0 1
-11 1
.names count[1] $add$counter.v:10$2_Y[1] en $procmux$3_Y[1]
1-0 1
-11 1
.names count[2] $add$counter.v:10$2_Y[2] en $procmux$3_Y[2]
1-0 1
-11 1
.names count[3] $add$counter.v:10$2_Y[3] en $procmux$3_Y[3]
1-0 1
-11 1
.names $procmux$3_Y[0] $false rst $0\count[3:0][0]
1-0 1
-11 1
.names $procmux$3_Y[1] $false rst $0\count[3:0][1]
1-0 1
-11 1
.names $procmux$3_Y[2] $false rst $0\count[3:0][2]
1-0 1
-11 1
.names $procmux$3_Y[3] $false rst $0\count[3:0][3]
1-0 1
-11 1
.latch $0\count[3:0][0] count[0] re clk 1
.latch $0\count[3:0][1] count[1] re clk 1
.latch $0\count[3:0][2] count[2] re clk 0
.latch $0\count[3:0][3] count[3] re clk 2
.names count[1] count[0] $techmap$add$counter.v:10$2.$auto$alumacc.cc:474:replace_alu$53.lcu.g[1]
11 1
.names count[2] $techmap$add$counter.v:10$2.$auto$alumacc.cc:474:replace_alu$53.lcu.g[1] $techmap$add$counter.v:10$2.$auto$alumacc.cc:474:replace_alu$53.lcu.g[2]
11 1
.names count[1] count[0] $add$counter.v:10$2_Y[1]
10 1
01 1
.names count[2] $techmap$add$counter.v:10$2.$auto$alumacc.cc:474:replace_alu$53.lcu.g[1] $add$counter.v:10$2_Y[2]
10 1
01 1
.names count[3] $techmap$add$counter.v:10$2.$auto$alumacc.cc:474:replace_alu$53.lcu.g[2] $add$counter.v:10$2_Y[3]
10 1
01 1
.names count[0] $true $add$counter.v:10$2_Y[0]
10 1
01 1
.names count[0] $techmap$add$counter.v:10$2.$auto$alumacc.cc:474:replace_alu$53.lcu.g[0]
1 1
.end
"""  # noqa

blif_with_output_as_arg = """
# Generated by Yosys 0.9+2406 (git sha1 aee43936, clang 11.0.3 -fPIC -Os)

.model Top
.inputs clk in[0] in[1]
.outputs out
.names $false
.names $true
1
.names $undef
.names out $techmap$add$test.v:9$6.$auto$alumacc.cc:485:replace_alu$60.X[0]
0 1
.names in[0] $not$test.v:6$1_Y[0]
0 1
.names r[0] $not$test.v:6$3_Y[0]
0 1
.latch $techmap$add$test.v:9$6.$auto$alumacc.cc:485:replace_alu$60.X[0] r[0] re clk 2
.names $not$test.v:6$1_Y[0] $not$test.v:6$3_Y[0] out
10 1
01 1
.names $true $not$test.v:6$3_Y[1]
1 1
.names $false $techmap$add$test.v:9$6.$auto$alumacc.cc:485:replace_alu$60.X[1]
1 1
.names $false $techmap$add$test.v:9$6.$auto$alumacc.cc:485:replace_alu$60.X[2]
1 1
.end
"""  # noqa


class TestInputFromBlif(unittest.TestCase):
    def setUp(self):
        pyrtl.reset_working_block()

    def test_combo_blif_input_has_correct_io_interface(self):
        pyrtl.input_from_blif(full_adder_blif)
        x, y, cin, sumw, cout, bad = [
            pyrtl.working_block().get_wirevector_by_name(s)
            for s in ['x', 'y', 'cin', 'sum', 'cout', 'bad']
        ]
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        self.assertIsNotNone(cin)
        self.assertIsNotNone(sumw)
        self.assertIsNotNone(cout)
        self.assertIsNone(bad)
        self.assertEquals(len(x), 1)
        self.assertEquals(len(y), 1)
        self.assertEquals(len(cin), 1)
        self.assertEquals(len(sumw), 1)
        self.assertEquals(len(cout), 1)
        io_input = pyrtl.working_block().wirevector_subset(pyrtl.Input)
        self.assertIn(x, io_input)
        self.assertIn(y, io_input)
        self.assertIn(cin, io_input)
        io_output = pyrtl.working_block().wirevector_subset(pyrtl.Output)
        self.assertIn(sumw, io_output)
        self.assertIn(cout, io_output)

    def test_sequential_blif_input_has_correct_io_interface(self):
        pyrtl.input_from_blif(state_machine_blif)
        inw, reset, out = [
            pyrtl.working_block().get_wirevector_by_name(s)
            for s in ['in', 'reset', 'out']
        ]
        self.assertIsNotNone(inw)
        self.assertIsNotNone(reset)
        self.assertIsNotNone(out)
        self.assertEquals(len(inw), 1)
        self.assertEquals(len(reset), 1)
        self.assertEquals(len(out), 4)
        io_input = pyrtl.working_block().wirevector_subset(pyrtl.Input)
        self.assertIn(inw, io_input)
        self.assertIn(reset, io_input)
        io_output = pyrtl.working_block().wirevector_subset(pyrtl.Output)
        self.assertIn(out, io_output)

    def test_sequential_blif_input_has_correct_io_interface_counter(self):
        pyrtl.input_from_blif(counter4bit_blif)
        rst, en, count = [
            pyrtl.working_block().get_wirevector_by_name(s)
            for s in ['rst', 'en', 'count']
        ]
        self.assertIsNotNone(rst)
        self.assertIsNotNone(en)
        self.assertIsNotNone(count)
        self.assertEquals(len(rst), 1)
        self.assertEquals(len(en), 1)
        self.assertEquals(len(count), 4)
        io_input = pyrtl.working_block().wirevector_subset(pyrtl.Input)
        self.assertIn(rst, io_input)
        self.assertIn(en, io_input)
        io_output = pyrtl.working_block().wirevector_subset(pyrtl.Output)
        self.assertIn(count, io_output)

    def test_blif_input_simulates_correctly_with_merged_outputs(self):
        # The 'counter_blif' string contains a model of a standard 4-bit synchronous-reset
        # counter with enable. In particular, the model has 4 1-bit outputs named "count[0]",
        # "count[1]", "count[2]", and "count[3]". The internal PyRTL representation will by
        # default convert these related 1-bit wires into a single 4-bit wire called "count".
        # This test simulates the design and, among other things, ensures that this output
        # wire conversion occurred correctly.
        pyrtl.input_from_blif(counter4bit_blif)
        io_vectors = pyrtl.working_block().wirevector_subset((pyrtl.Input, pyrtl.Output))
        sim_trace = pyrtl.SimulationTrace(wires_to_track=io_vectors)
        sim = pyrtl.Simulation(sim_trace)
        inputs = {
            'rst': [1] + [0] * 20,
            'en': [1] + [1] * 20,
        }
        expected = {
            'count': [0] + list(range(0, 16)) + list(range(0, 4))
        }
        sim.step_multiple(inputs, expected)

        correct_output = ("  --- Values in base 10 ---\n"
                          "count  0  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15  0  1  2  3\n"
                          "en     1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1\n"
                          "rst    1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n")
        output = six.StringIO()
        sim_trace.print_trace(output)
        self.assertEqual(output.getvalue(), correct_output)

    def test_sequential_blif_input_fails_to_parse_with_bad_latch_init(self):
        with self.assertRaises(pyrtl.PyrtlError):
            pyrtl.input_from_blif(counter4bit_blif_bad_latch_inits)

    def test_blif_with_output_as_arg(self):
        pyrtl.input_from_blif(blif_with_output_as_arg)
        inw, outw = [
            pyrtl.working_block().get_wirevector_by_name(s)
            for s in ['in', 'out']
        ]
        self.assertIsNotNone(inw)
        self.assertIsNotNone(outw)
        self.assertEquals(len(inw), 2)
        self.assertEquals(len(outw), 1)
        io_input = pyrtl.working_block().wirevector_subset(pyrtl.Input)
        self.assertIn(inw, io_input)
        io_output = pyrtl.working_block().wirevector_subset(pyrtl.Output)
        self.assertIn(outw, io_output)


class TestOutputGraphs(unittest.TestCase):
    def setUp(self):
        pyrtl.reset_working_block()

    def test_output_to_tgf_does_not_throw_error(self):
        with io.StringIO() as vfile:
            pyrtl.input_from_blif(full_adder_blif)
            pyrtl.output_to_trivialgraph(vfile)

    def test_output_to_graphviz_does_not_throw_error(self):
        with io.StringIO() as vfile:
            pyrtl.input_from_blif(full_adder_blif)
            pyrtl.output_to_graphviz(vfile)

    def test_output_to_graphviz_with_custom_namer_does_not_throw_error(self):
        with io.StringIO() as vfile:
            pyrtl.input_from_blif(full_adder_blif)
            timing = analysis.TimingAnalysis()
            node_fan_in = {net: len(net.args) for net in pyrtl.working_block()}
            graph_namer = pyrtl.inputoutput.graphviz_detailed_namer(
                extra_node_info=node_fan_in,
                extra_edge_info=timing.timing_map
            )
            pyrtl.output_to_graphviz(vfile, namer=graph_namer)


class TestNetGraph(unittest.TestCase):
    def setUp(self):
        pyrtl.reset_working_block()

    def test_as_graph(self):
        inwire = pyrtl.Input(bitwidth=1, name="inwire1")
        inwire2 = pyrtl.Input(bitwidth=1)
        inwire3 = pyrtl.Input(bitwidth=1)
        tempwire = pyrtl.WireVector()
        tempwire2 = pyrtl.WireVector()
        outwire = pyrtl.Output()

        tempwire <<= inwire | inwire2
        tempwire2 <<= ~tempwire
        outwire <<= tempwire2 & inwire3

        g = inputoutput.net_graph()
        # note for future: this might fail if we change
        # the way that temp wires are inserted, but that
        # should not matter for this test and so the number
        # can be safely updated.
        self.assertEqual(len(g), 10)

    def test_netgraph_unused_wires(self):
        genwire = pyrtl.WireVector(8, "genwire")
        inwire = pyrtl.Input(8, "inwire")
        outwire = pyrtl.Output(8, "outwire")
        constwire = pyrtl.Const(8, 8)
        reg = pyrtl.Register(8, "reg")
        g = inputoutput.net_graph()
        self.assertEquals(len(g), 0)


class TestOutputIPynb(unittest.TestCase):
    def setUp(self):
        pyrtl.reset_working_block()
        self.maxDiff = None

    def test_one_bit_adder_matches_expected(self):
        temp1 = pyrtl.WireVector(bitwidth=1, name='temp1')
        temp2 = pyrtl.WireVector()

        a, b, c = pyrtl.Input(1, 'a'), pyrtl.Input(1, 'b'), pyrtl.Input(1, 'c')
        sum, carry_out = pyrtl.Output(1, 'sum'), pyrtl.Output(1, 'carry_out')

        sum <<= a ^ b ^ c

        temp1 <<= a & b  # connect the result of a & b to the pre-allocated wirevector
        temp2 <<= a & c
        temp3 = b & c  # temp3 IS the result of b & c (this is the first mention of temp3)
        carry_out <<= temp1 | temp2 | temp3

        sim_trace = pyrtl.SimulationTrace()
        sim = pyrtl.Simulation(tracer=sim_trace)
        for cycle in range(15):
            sim.step({
                'a': random.choice([0, 1]),
                'b': random.choice([0, 1]),
                'c': random.choice([0, 1])
            })

        htmlstring = inputoutput.trace_to_html(sim_trace)  # tests if it compiles or not


firrtl_output_concat_test = """\
circuit Example :
  module Example :
    input clock : Clock
    input reset : UInt<1>
    output o : UInt<13>
    wire tmp0 : UInt<13>
    wire tmp1 : UInt<7>
    wire tmp2 : UInt<13>
    node const_0_12 = UInt<4>(12)
    node const_1_3 = UInt<3>(3)
    node const_2_38 = UInt<6>(38)

    o <= tmp0
    tmp0 <= tmp2
    tmp1 <= cat(const_0_12, const_1_3)
    tmp2 <= cat(tmp1, const_2_38)
"""

firrtl_output_select_test = """\
circuit Example :
  module Example :
    input clock : Clock
    input reset : UInt<1>
    output b : UInt<6>
    wire tmp0 : UInt<6>
    wire tmp1 : UInt<1>
    wire tmp2 : UInt<1>
    wire tmp3 : UInt<1>
    wire tmp4 : UInt<1>
    wire tmp5 : UInt<1>
    wire tmp6 : UInt<1>
    wire tmp7 : UInt<6>
    wire tmp8 : UInt<2>
    wire tmp9 : UInt<3>
    wire tmp10 : UInt<4>
    wire tmp11 : UInt<5>
    wire tmp12 : UInt<6>
    node const_0_2893 = UInt<12>(2893)

    b <= tmp0
    tmp0 <= tmp7
    tmp1 <= bits(const_0_2893, 0, 0)
    tmp2 <= bits(const_0_2893, 2, 2)
    tmp3 <= bits(const_0_2893, 4, 4)
    tmp4 <= bits(const_0_2893, 6, 6)
    tmp5 <= bits(const_0_2893, 8, 8)
    tmp6 <= bits(const_0_2893, 10, 10)
    tmp7 <= tmp12
    tmp8 <= cat(tmp6, tmp5)
    tmp9 <= cat(tmp8, tmp4)
    tmp10 <= cat(tmp9, tmp3)
    tmp11 <= cat(tmp10, tmp2)
    tmp12 <= cat(tmp11, tmp1)
"""


class TestOutputFirrtl(unittest.TestCase):
    def setUp(self):
        pyrtl.reset_working_block()
        pyrtl.wire._reset_wire_indexers()
        pyrtl.memory._reset_memory_indexer()

    def test_textual_consistency_concats(self):
        i = pyrtl.Const(0b1100)
        j = pyrtl.Const(0b011, bitwidth=3)
        k = pyrtl.Const(0b100110)
        o = pyrtl.Output(13, 'o')
        o <<= pyrtl.concat(i, j, k)

        buffer = io.StringIO()
        pyrtl.output_to_firrtl(buffer)

        self.assertEqual(buffer.getvalue(), firrtl_output_concat_test)

    def test_textual_consistency_selects(self):
        a = pyrtl.Const(0b101101001101)
        b = pyrtl.Output(6, 'b')
        b <<= a[::2]

        buffer = io.StringIO()
        pyrtl.output_to_firrtl(buffer)

        self.assertEqual(buffer.getvalue(), firrtl_output_select_test)


if __name__ == "__main__":
    unittest.main()
