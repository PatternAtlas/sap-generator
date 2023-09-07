from typing import List
from aggregation_step import AggregationStep

def print_aggregation_steps(aggregation_steps: List[AggregationStep]):
    for idx, aggregation_step in enumerate(aggregation_steps):
        print(f"Aggregation Step {idx+1}: \n Operator: {aggregation_step.operator}, \n \
            Mapping: {aggregation_step.mapping}, \n \
            AggregateId: {aggregation_step.aggregate.id}, \n \
            AggregateType: {aggregation_step.aggregate.cs_type}")