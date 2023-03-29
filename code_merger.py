import argparse
import matplotlib.pyplot as plt
import os
import queue
import itertools
import time
import pyclip


def get_header(line: str, char_left: str, char_right: str) -> str:
    if not line.startswith("#include"):
        return ""
    line = line.removeprefix("#include").lstrip()
    if len(line) == 0 or line[0] != char_left:
        return ""
    return line.split(char_left)[1].split(char_right)[0]


def get_user_header(line: str) -> str:
    return get_header(line, "\"", "\"")


def get_system_header(line: str) -> str:
    return get_header(line, "<", ">")


def is_any_header(line: str) -> str:
    return line.startswith("#include")


class Merger:
    def __init__(self) -> None:
        self.graph = None
        self.order = None

    def generate_code(self, main_file: str) -> str:
        self.generate_graph(main_file)
        self.generate_order()

        code_lines = []
        before_include_lines = []
        include_lines = []

        DEFINES_PATH = "src/defines.hpp"
        if DEFINES_PATH in self.order:
            self.order.remove(DEFINES_PATH)

            with open(DEFINES_PATH, "r") as file:
                lines = file.readlines()

            try:
                idx = lines.index("// PASTE ALL INCLUDES!\n")
            except ValueError:
                print(f"ERROR:// PASTE ALL INCLUDES!\n must be inside defines!")
                exit(0)

            before_include_lines.extend(lines[:idx])
            code_lines.extend(lines[idx+1:])
            code_lines.extend("\n")

        for filename in self.order:
            with open(filename, "r") as file:
                lines = file.readlines()

            code_lines.extend(itertools.filterfalse(is_any_header, lines))
            code_lines.extend("\n")
            include_lines.extend(filter(lambda x: len(x) > 0,
                                        filter(get_system_header, lines)))

        include_lines = list(sorted(set(include_lines)))

        return "".join(before_include_lines) + \
            "".join(include_lines) + \
            "".join(code_lines)

    def generate_graph(self, main_file: str) -> None:
        self.graph = {}

        def parse_file(filename: str) -> None:

            if filename in self.graph:
                return

            print(f"Parsing file {filename}.")
            self.graph[filename] = set()

            with open(filename, "r") as file:
                lines = file.readlines()

            for line in filter(lambda x: len(x) > 0, filter(get_user_header, lines)):
                user_header = get_user_header(line)
                self.graph[filename].add(user_header)
                print(f"Edge from {filename} -> {user_header}.")

            # check for .cpp file.
            if filename.endswith(".hpp"):
                source_file = filename.removesuffix(".hpp") + ".cpp"
                if os.path.exists(source_file):
                    parse_file(source_file)

            for file in self.graph[filename]:
                parse_file(file)

        parse_file(main_file)

    def generate_order(self) -> None:
        graphR = {u: set() for u in self.graph.keys()}
        in_deg = {u: 0 for u in self.graph.keys()}

        for u in self.graph.keys():
            for v in self.graph[u]:
                graphR[v].add(u)
                in_deg[u] += 1

        order = []

        q = queue.Queue()

        for u in in_deg.keys():
            if in_deg[u] == 0:
                q.put(u)

        while not q.empty():
            u = q.get()
            order.append(u)

            for v in graphR[u]:
                in_deg[v] -= 1

                if in_deg[v] == 0:
                    q.put(v)

        if len(order) != len(in_deg):
            print("There is a cycle in includes!")
            exit(1)

        print("Order of files:", *order, sep='\n')
        self.order = order


def draw_graph(graph: dict[str, set]) -> None:
    import networkx as nx

    print(graph)
    G = nx.DiGraph()
    G.add_nodes_from(graph.keys())
    for file, edges in graph.items():
        for e in edges:
            G.add_edge(file, e)

    def calc_size(file: str) -> int:
        with open(file, "r") as file:
            return len(file.readlines()) * 10

    node_sizes = [calc_size(file) for file in G.nodes]

    options = {
        'with_labels': True,
        'arrows': True,
        'font_color': 'black',
        'font_weight': 'bold',
        'font_size': 20,
        'node_color': 'yellow',
        'node_size': node_sizes,
        'arrowstyle': '-|>',
        'arrowsize': 20,
        'width': 2,
        'edge_color': 'green',
    }

    nx.draw_networkx(G, **options)
    plt.show()
    return


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
            Program to merge many c++ files into one .cpp file.
            It splits main file into 'before first include' and after.
            First it write 'before first include' to out, then all dependencies
            and finally main after first include.
        """
    )

    parser.add_argument("main", type=str, help="Main file to merge.")

    parser.add_argument("--draw", action=argparse.BooleanOptionalAction)

    parser.add_argument("--name", type=str, help="Name for merged code.")

    global args
    args = parser.parse_args()

    merger = Merger()
    code = merger.generate_code(args.main)

    if args.draw:
        draw_graph(merger.graph)

    pyclip.copy(code)

    if args.name is None:
        args.name = os.path.splitext(os.path.basename(args.main))[0]

    date = time.strftime("%Y:%m:%d-%H:%M:%S")
    with open(f"codes/{args.name}-{date}.cpp", "w") as file:
        file.write(f"// {args.name}-{date}\n")
        file.write(code)


if __name__ == "__main__":
    main()
