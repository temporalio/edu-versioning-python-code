import asyncio
import logging

from shared import TASK_QUEUE_NAME, WORKFLOW_ID_PREFIX, create_pizza_order
from temporalio.client import Client, BuildIdOpAddNewDefault
from workflow import PizzaOrderWorkflow


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233", namespace="default")

    await client.update_worker_build_id_compatibility(
        TASK_QUEUE_NAME, BuildIdOpAddNewDefault("revision-yymmdd")
    )

    order = create_pizza_order()

    # Execute a workflow
    handle = await client.start_workflow(
        PizzaOrderWorkflow.order_pizza,
        order,
        id=WORKFLOW_ID_PREFIX + order.order_number,
        task_queue=TASK_QUEUE_NAME,
    )

    result = await handle.result()

    logging.info(f"Result:\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
