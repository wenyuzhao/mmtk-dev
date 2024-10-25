# ./scripts/ebpf/heat.py --gc ix --bench lusearch --json > lusearch-ix.jsonl
# ./scripts/ebpf/heat.py --gc lxr --bench lusearch --json > lusearch-lxr.jsonl
# ./scripts/ebpf/heat.py --gc g1 --bench lusearch --json > lusearch-g1.jsonl
# ./scripts/ebpf/heat.py --gc shen --bench lusearch --json > lusearch-shen.jsonl
# ./scripts/ebpf/heat.py --gc z --bench lusearch --json > lusearch-z.jsonl
 ./scripts/ebpf/heat.py --gc par --bench lusearch --json > lusearch-par.jsonl

# ./scripts/ebpf/heat.py --gc ix --bench h2 --json > h2-ix.jsonl
# ./scripts/ebpf/heat.py --gc lxr --bench h2 --json > h2-lxr.jsonl
# ./scripts/ebpf/heat.py --gc g1 --bench h2 --json > h2-g1.jsonl
# ./scripts/ebpf/heat.py --gc shen --bench h2 --json > h2-shen.jsonl
# ./scripts/ebpf/heat.py --gc z --bench h2 --json > h2-z.jsonl
./scripts/ebpf/heat.py --gc par --bench h2 --json > h2-par.jsonl


# ./scripts/ebpf/heat.py --gc ix --bench kafka --json > kafka-ix.jsonl
# ./scripts/ebpf/heat.py --gc lxr --bench kafka --json > kafka-lxr.jsonl
# ./scripts/ebpf/heat.py --gc g1 --bench kafka --json > kafka-g1.jsonl
# ./scripts/ebpf/heat.py --gc shen --bench kafka --json > kafka-shen.jsonl
# ./scripts/ebpf/heat.py --gc z --bench kafka --json > kafka-z.jsonl
./scripts/ebpf/heat.py --gc par --bench kafka --json > kafka-par.jsonl