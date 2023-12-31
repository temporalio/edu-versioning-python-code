import asyncio
import logging

from shared import TASK_QUEUE_NAME, WORKFLOW_ID_PREFIX, create_pizza_order
from temporalio.client import Client, BuildIdOpAddNewDefault
from workflow import PizzaOrderWorkflow


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233", namespace="default")

    # TODO Part A: call client.update_worker_build_id_compatibility() to inform the
    # Task Queue of your Build ID. You can also do this via the CLI if you are
    # changing a currently running workflow. An example of how to do it via the SDK
    # is below. Don't forget to change the BuildID to match your Worker.
    #
    # await client.update_worker_build_id_compatibility(
    #     TASK_QUEUE_NAME, BuildIdOpAddNewDefault("revision-yymmdd")
    # )
    # **Note:** This code would usually only need to be run once. In a production
    # system you would not run this as part of your client, but more likely as part
    # of your build system on initial deployment, either via the SDK or the CLI.

    order = create_pizza_order()

    # Execute a workflow
    handle = await client.start_workflow(
        PizzaOrderWorkflow.order_pizza,
        order,
        id=WORKFLOW_ID_PREFIX + f"{order.order_number}",
        task_queue=TASK_QUEUE_NAME,
    )

    result = await handle.result()

    logging.info(f"Result:\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
