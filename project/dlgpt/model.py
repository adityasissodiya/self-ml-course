# STUB
"""P8-P9 - the transformer block and the decoder-only GPT.

  P8 (concept 12): TransformerBlock = residual + LayerNorm + FFN; stack N of them.
  P9 (concept 13): GPT with an LM head + greedy/temperature/top-k generation.

Flip the first line to "# AUTHORED" once you start implementing.
"""


class TransformerBlock:
    """Pre-norm transformer block: x + attn(ln(x)), then x + ffn(ln(x)). (P8)"""

    def __init__(self, d_model, num_heads):
        raise NotImplementedError("P8: implement TransformerBlock - concept 12")

    def __call__(self, x):
        raise NotImplementedError("P8: implement TransformerBlock.__call__")


class GPT:
    """Decoder-only language model: embeddings + N blocks + LM head. (P9)"""

    def __init__(self, vocab_size, d_model, num_heads, num_layers, block_size):
        raise NotImplementedError("P9: implement GPT - concept 13")

    def __call__(self, idx):
        raise NotImplementedError("P9: implement GPT.__call__ (logits)")


def generate(model, idx, max_new_tokens, temperature=1.0, top_k=None):
    """Autoregressively sample `max_new_tokens` new ids. (P9)"""
    raise NotImplementedError("P9: implement generate - concept 13")
