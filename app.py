import multiprocessing

from flows.docongso.FlowDocongso import FlowDocongso


def main(flows):
    processes = []
    for flow in flows:
        processes += [multiprocessing.Process(target=flow.Run)]

    for proc in processes:
        proc.start()


if __name__ == "__main__":
    print("Admin started")
    flows = [
        FlowDocongso(),
    ]

    main(flows)
