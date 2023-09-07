import unittest

from graph import Graph
from subgraph_operator import Operator, Operation
from solution import Solution
from algebra import SolutionAlgebra
from mapping import Mapping

from typing import List
from algo import calc_aggregation_based_on_subgraphs, create_joined_permuation, get_aggregator_permutations

from helpers import print_aggregation_steps

class Tests(unittest.TestCase):

    @unittest.skip("not now")
    def test_create_joined_permuation(self):
        list1 = [[1, 2], [3, 4]]
        list2 = [[5, 6], [7, 8]]
        list3 = [[9, 10], [11, 12]]
        result = create_joined_permuation([list1, list2, list3])
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 8)

    @unittest.skip("not now")
    def test_get_aggregator_permutations(self):
        op1 = Operator(None, None, 3)
        op2 = Operator(None, None, 2)
        op3 = Operator(None, None, 2)
        op4 = Operator(None, None, 2)
        op5 = Operator(None, None, 1)
        op6 = Operator(None, None, 1)
        operators = set([op1, op2, op3, op4, op5, op6])
        aggregator_permutations = get_aggregator_permutations(operators)
        self.assertEqual(len(list(aggregator_permutations)), 12)
    
    @unittest.skip("not now")
    def test_two_nodes_one_operator_one_supported_subgraph(self):
        cs1 = Solution(id=1,
                       requirements=set(),
                       capabilities=set({"logged_in"}),
                       cs_type="type1")
        cs2 = Solution(id=2,
                       requirements=set({"logged_in"}),
                       capabilities=set(),
                       cs_type="type1")
        
        cs1_operator1 = Solution(id="op1_cs1", requirements=set(), capabilities=set({"logged_in"}), cs_type="type1")
        cs2_operator1 = Solution(id="op1_cs2", requirements=set({"logged_in"}), capabilities=set(), cs_type="type1")

        operator_nodes = [cs1_operator1, cs2_operator1]
        operator_edges = [{cs1_operator1, cs2_operator1}]
        operator_detector_graph = Graph(operator_nodes, operator_edges)

        def operator_function(mapping: Mapping) -> Solution:
            solutions = mapping.get_detected_solutions()
            cs_id = ""
            for solution in solutions:
                cs_id += str(solution.id)
            solution = Solution(cs_id, requirements=set(), capabilities=set({"logged_in"}), cs_type="type1")
            return solution


        operator1 = Operator(supported_operations=[Operation(operator_detector_graph, operator_function)],
                             aggregate_type="type1",
                             rank=0)
        
        algebra = SolutionAlgebra(solutions=[cs1, cs2],
                                  operators=[operator1])
        
        solution_graph_nodes = [cs1, cs2]
        solution_graph_edges = [{cs1, cs2}]
        solution_graph = Graph(solution_graph_nodes, solution_graph_edges)
        complete_aggregation_steps = []
        incompleted_aggregations = []
        calc_aggregation_based_on_subgraphs(solution_graph, [],
                                            algebra.operators,
                                            complete_aggregation_steps,
                                            incompleted_aggregations)
        print("Test Scenario two nodes one operator")
        for idx, aggregation_steps in enumerate(complete_aggregation_steps):
            print(f"Aggregation {idx+1}:")
            print_aggregation_steps(aggregation_steps)
        self.assertEqual(len(complete_aggregation_steps), 1)
        self.assertEqual(len(complete_aggregation_steps[0]), 1)

    @unittest.skip("not now")
    def test_two_nodes_one_operator_two_supported_subgraphs(self):
        cs1 = Solution(id=1,
                       requirements=set(),
                       capabilities=set({"logged_in"}),
                       cs_type="type1")
        cs2 = Solution(id=2,
                       requirements=set({"logged_in"}),
                       capabilities=set(),
                       cs_type="type1")
        
        cs1_operator1 = Solution(id="op1_cs1", requirements=set({"password"}), capabilities=set({"logged_in"}), cs_type="type1")
        cs2_operator1 = Solution(id="op1_cs2", requirements=set(), capabilities=set({"password"}), cs_type="type1")
        subgraph1_nodes = [cs1_operator1, cs2_operator1]
        subgraph1_edges = [{cs1_operator1, cs2_operator1}]
        operator_detector_graph1 = Graph(subgraph1_nodes, subgraph1_edges)
        def operator_function1(mapping: Mapping) -> Solution:
            solutions = mapping.get_detected_solutions()
            cs_id = ""
            for solution in solutions:
                cs_id += str(solution.id)
            solution = Solution(cs_id, requirements=set(), capabilities=set({"logged_in"}), cs_type="type1")
            return solution
        supported_operation1 = Operation(operator_detector_graph1, operator_function1)

        cs3_operator1 = Solution(id="op1_cs3", requirements=set(), capabilities=set({"logged_in"}), cs_type="type1")
        cs4_operator1 = Solution(id="op1_cs4", requirements=set({"logged_in"}), capabilities=set(), cs_type="type1")
        subgraph2_nodes = [cs3_operator1, cs4_operator1]
        subgraph2_edges = [{cs3_operator1, cs4_operator1}]
        operator_detector_graph2 = Graph(subgraph2_nodes, subgraph2_edges)
        def operator_function2(mapping: Mapping) -> Solution:
            solutions = mapping.get_detected_solutions()
            cs_id = ""
            for solution in solutions:
                cs_id += str(solution.id)
            solution = Solution(cs_id, requirements=set(), capabilities=set({"shell"}), cs_type="type1")
            return solution
        supported_operation2 = Operation(operator_detector_graph2, operator_function2)

        operator1 = Operator(supported_operations=[supported_operation1, supported_operation2],
                             aggregate_type="type1",
                             rank=0)
        
        algebra = SolutionAlgebra(solutions=[cs1, cs2],
                                  operators=[operator1])
        
        solution_graph_nodes = [cs1, cs2]
        solution_graph_edges = [{cs1, cs2}]
        solution_graph = Graph(solution_graph_nodes, solution_graph_edges)
        complete_aggregation_steps = []
        incompleted_aggregations = []
        calc_aggregation_based_on_subgraphs(solution_graph, [],
                                            algebra.operators,
                                            complete_aggregation_steps,
                                            incompleted_aggregations)
        print("Test Scenario two_nodes_one_operator_two_supported_subgraphs")
        for idx, aggregation_steps in enumerate(complete_aggregation_steps):
            print(f"Aggregation {idx+1}:")
            print_aggregation_steps(aggregation_steps)
        self.assertEqual(len(complete_aggregation_steps), 1)
        self.assertEqual(len(complete_aggregation_steps[0]), 1)

    @unittest.skip("not now")
    def test_three_nodes_one_operator(self):
        cs1 = Solution(id="cs1",
                       requirements=set({"password"}),
                       capabilities=set({"logged_in"}),
                       cs_type="type1")
        cs2 = Solution(id="cs2",
                       requirements=set({"logged_in"}),
                       capabilities=set(),
                       cs_type="type1")
        cs3 = Solution(id="cs3",
                       requirements=set(),
                       capabilities=set({"password"}),
                       cs_type="type1")
        
        cs1_operator1 = Solution(id="op1_cs1", requirements=set({"password"}), capabilities=set({"logged_in"}), cs_type="type1")
        cs2_operator1 = Solution(id="op1_cs2", requirements=set(), capabilities=set({"password"}), cs_type="type1")
        subgraph1_nodes = [cs1_operator1, cs2_operator1]
        subgraph1_edges = [{cs1_operator1, cs2_operator1}]
        operator_detector_graph1 = Graph(subgraph1_nodes, subgraph1_edges)
        def operator_function1(mapping: Mapping) -> Solution:
            solutions = mapping.get_detected_solutions()
            cs_id = ""
            for solution in solutions:
                cs_id += str(solution.id)
            solution = Solution(cs_id, requirements=set(), capabilities=set({"logged_in"}), cs_type="type1")
            return solution
        supported_operation1 = Operation(operator_detector_graph1, operator_function1)

        cs3_operator1 = Solution(id="op1_cs3", requirements=set({"logged_in"}), capabilities=set(), cs_type="type1")
        cs4_operator1 = Solution(id="op1_cs4", requirements=set(), capabilities=set({"logged_in"}), cs_type="type1")
        subgraph2_nodes = [cs3_operator1, cs4_operator1]
        subgraph2_edges = [{cs3_operator1, cs4_operator1}]
        operator_detector_graph2 = Graph(subgraph2_nodes, subgraph2_edges)
        def operator_function2(mapping: Mapping) -> Solution:
            solutions = mapping.get_detected_solutions()
            cs_id = ""
            for solution in solutions:
                cs_id += str(solution.id)
            solution = Solution(cs_id, requirements=set(), capabilities=set({"shell"}), cs_type="type1")
            return solution
        supported_operation2 = Operation(operator_detector_graph2, operator_function2)

        supported_operations = [supported_operation1, supported_operation2]

        operator1 = Operator(supported_operations=supported_operations,
                             aggregate_type="type1",
                             rank=0)
        
        algebra = SolutionAlgebra(solutions=[cs1, cs2, cs3],
                                  operators=[operator1])
        
        solution_graph_nodes = [cs1, cs2, cs3]
        solution_graph_edges = [{cs1, cs2}, {cs1, cs3}]
        solution_graph = Graph(solution_graph_nodes, solution_graph_edges)
        complete_aggregation_steps = []
        incompleted_aggregations = []
        calc_aggregation_based_on_subgraphs(solution_graph, [],
                                            algebra.operators,
                                            complete_aggregation_steps,
                                            incompleted_aggregations)
        print("Test Scenario two nodes one operator")
        for idx, aggregation_steps in enumerate(complete_aggregation_steps):
            print(f"Aggregation {idx+1}:")
            print_aggregation_steps(aggregation_steps)
        self.assertEqual(len(complete_aggregation_steps), 1)
        self.assertEqual(len(complete_aggregation_steps[0]), 2)

    def test_many_nodes_many_edges_multiple_operators(self):
        solutions = []
        for i in range(30):
            solution = Solution(id=i,
                                requirements=set(),
                                capabilities=set(),
                                cs_type="type1")
            solutions.append(solution)
        
        # create edges between all solutions
        solution_graph_edges = []
        for i in range(len(solutions)):
            for j in range(i+1, len(solutions)):
                solution_graph_edges.append({solutions[i], solutions[j]})

        solution_graph = Graph(solutions, solution_graph_edges)

        # create operators
        operators = []
        for i in range(2):
            supported_operations = []
            detector_solution1 = Solution(id="op" + str(i) + "_1", requirements=set(), capabilities=set(), cs_type="type1")
            detector_solution2 = Solution(id="op" + str(i)  + "_2", requirements=set(), capabilities=set(), cs_type="type1")
            
            def aggregation_function(mapping: Mapping) -> Solution:
                solutions = mapping.get_detected_solutions()
                cs_id = ""
                for solution in solutions:
                    cs_id += str(solution.id)
                return Solution(id=cs_id, requirements=set(), capabilities=set(), cs_type="type1")
            
            operation = Operation(
                graph=Graph(
                    solutions=[detector_solution1, detector_solution2],
                    edges=[{detector_solution1, detector_solution2}]
                ),
                operation=aggregation_function)
            supported_operations.append(operation)
            operator = Operator(supported_operations=supported_operations,
                                aggregate_type="type1",
                                rank=0)
            operators.append(operator)
        
        algebra = SolutionAlgebra(solutions=solutions,
                                  operators=operators)
        
        complete_aggregation_steps = []
        incompleted_aggregations = []

        calc_aggregation_based_on_subgraphs(solution_graph, [],
                                            algebra.operators,
                                            complete_aggregation_steps,
                                            incompleted_aggregations)
        print("Test Scenario complex")
        for idx, aggregation_steps in enumerate(complete_aggregation_steps):
            print(f"Aggregation {idx+1}:")
            print_aggregation_steps(aggregation_steps)
        if len(complete_aggregation_steps) == 0:
            print("something went wrong")
        self.assertEqual(len(complete_aggregation_steps), 1)

import cProfile
import pstats
import sys
print(sys.path)

if __name__ == '__main__':
    unittest.main()
    # cProfile.run('Tests().test_three_nodes_one_operator()', filename='profile.prof')
    # stats = pstats.Stats('profile.prof')
    # stats.strip_dirs().sort_stats('cumulative').print_stats(10)