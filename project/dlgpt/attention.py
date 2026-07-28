# STUB
"""P4-P7 - attention machinery.

  P4 (concept 08): scaled dot-product self-attention.
  P5 (concept 09): causal masking (no future leakage).
  P6 (concept 10): multi-head attention (parallel heads, concat + projection).
  P7 (concept 11): positional encoding added to embeddings.

Flip the first line to "# AUTHORED" once you start implementing.
"""


def self_attention(Q, K, V):
    """Scaled dot-product attention: softmax(Q Kᵀ / sqrt(d)) V. (P4)"""
    raise NotImplementedError("P4: implement self_attention - concept 08")


def causal_mask(scores):
    """Set scores[i][j] = -inf for j > i (no attending to the future). (P5)"""
    raise NotImplementedError("P5: implement causal_mask - concept 09")


def multi_head_attention(x, num_heads):
    """Run `num_heads` attention heads in parallel, concat, project. (P6)"""
    raise NotImplementedError("P6: implement multi_head_attention - concept 10")


def positional_encoding(seq_len, d_model):
    """Return a (seq_len, d_model) table of positional encodings. (P7)"""
    raise NotImplementedError("P7: implement positional_encoding - concept 11")
