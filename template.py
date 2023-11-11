r"""
Supports language model inference without histories.
"""
register_template(
    name="vanilla",
    prefix=[],
    prompt=["{{query}}"],
    system="",
    sep=[],
    use_history=False,
)


r"""
Default template.
"""
register_template(
    name="default",
    prefix=["{{system}}"],
    prompt=["Human: {{query}}\nAssistant: "],
    system=(
        "A chat between a curious user and an artificial intelligence assistant. "
        "The assistant gives helpful, detailed, and polite answers to the user's questions."
    ),
    sep=["\n"],
)


r"""
Supports: https://huggingface.co/meta-llama/Llama-2-7b-chat-hf
          https://huggingface.co/meta-llama/Llama-2-13b-chat-hf
          https://huggingface.co/meta-llama/Llama-2-70b-chat-hf
"""
register_template(
    name="llama2",
    prefix=["<<SYS>>\n{{system}}\n<</SYS>>\n\n"],
    prompt=["[INST] {{query}} [/INST]"],
    system=(
        "You are a helpful, respectful and honest assistant. "
        "Always answer as helpfully as possible, while being safe. "
        "Your answers should not include any harmful, unethical, "
        "racist, sexist, toxic, dangerous, or illegal content. "
        "Please ensure that your responses are socially unbiased and positive in nature.\n"
        "If a question does not make any sense, or is not factually coherent, "
        "explain why instead of answering something not correct. "
        "If you don't know the answer to a question, please don't share false information."
    ),
    sep=[],
)


r"""
Supports: https://github.com/ymcui/Chinese-LLaMA-Alpaca-2
          https://huggingface.co/ziqingyang/chinese-alpaca-2-7b
"""
register_template(
    name="llama2_zh",
    prefix=["<<SYS>>\n{{system}}\n<</SYS>>\n\n"],
    prompt=["[INST] {{query}} [/INST] "],
    system="You are a helpful assistant. 你是一个乐于助人的助手。",
    sep=[],
)


r"""
Supports: https://huggingface.co/tatsu-lab/alpaca-7b-wdiff
          https://github.com/ymcui/Chinese-LLaMA-Alpaca
"""
register_template(
    name="alpaca",
    prefix=["{{system}}"],
    prompt=["### Instruction:\n{{query}}\n\n### Response:\n"],
    system=(
        "Below is an instruction that describes a task. "
        "Write a response that appropriately completes the request."
    ),
    sep=["\n\n"],
)


r"""
Supports: https://huggingface.co/lmsys/vicuna-7b-delta-v1.1
          https://huggingface.co/lmsys/vicuna-13b-delta-v1.1
"""
register_template(
    name="vicuna",
    prefix=["{{system}}"],
    prompt=["USER: {{query}} ASSISTANT: "],
    system=(
        "A chat between a curious user and an artificial intelligence assistant. "
        "The assistant gives helpful, detailed, and polite answers to the user's questions."
    ),
    sep=[],
)


r"""
Supports: https://huggingface.co/BelleGroup/BELLE-LLaMA-EXT-13B
"""
register_template(
    name="belle",
    prefix=["{{system}}"],
    prompt=["Human: {{query}}\n\nBelle: "],
    system="",
    sep=["\n\n"],
)


r"""
Supports: https://github.com/CVI-SZU/Linly
"""
register_template(
    name="linly",
    prefix=["{{system}}"],
    prompt=["User: {{query}}\nBot: "],
    system="",
    sep=["\n"],
)


r"""
Supports: https://github.com/Neutralzz/BiLLa
"""
register_template(
    name="billa",
    prefix=["{{system}}"],
    prompt=["Human: {{query}}\nAssistant: "],
    system="",
    sep=["\n"],
)


r"""
Supports: https://huggingface.co/IDEA-CCNL/Ziya-LLaMA-13B-v1
"""
register_template(
    name="ziya",
    prefix=["{{system}}"],
    prompt=[{"token": "<human>"}, ":{{query}}\n", {"token": "<bot>"}, ":"],
    system="",
    sep=["\n"],
)


r"""
Supports: https://huggingface.co/qhduan/aquilachat-7b
"""
register_template(
    name="aquila",
    prefix=["{{system}}"],
    prompt=["Human: {{query}}###Assistant: "],
    system=(
        "A chat between a curious human and an artificial intelligence assistant. "
        "The assistant gives helpful, detailed, and polite answers to the human's questions."
    ),
    sep=["###"],
)


r"""
Supports: https://huggingface.co/internlm/internlm-chat-7b
"""
register_template(
    name="intern",
    prefix=["{{system}}"],
    prompt=["<|User|>:{{query}}", {"token": "<eoh>"}, "\n<|Bot|>:"],
    system="",
    sep=["\n"],
    stop_words=["</s>", "<eoa>"],  # internlm cannot replace eos token
)


r"""
Supports: https://huggingface.co/baichuan-inc/Baichuan-13B-Chat
Used for training and inference of the fine-tuned models.
"""
register_template(
    name="baichuan",
    prefix=["{{system}}"],
    prompt=[
        {"token": "<reserved_102>"},  # user token
        "{{query}}",
        {"token": "<reserved_103>"},  # assistant token
    ],
    system="",
    sep=[],
    stop_words=[],
)


r"""
Supports: https://huggingface.co/baichuan-inc/Baichuan-13B-Chat
Used for inference of the original model.
"""
register_template(
    name="baichuan_eval",
    prefix=["{{system}}", {"token": "<reserved_102>"}],  # user token
    prompt=["{{query}}", {"token": "<reserved_103>"}],  # assistant token
    system="",
    sep=[],
    stop_words=["<reserved_102>"],  # user token
)

r"""
Supports: https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat
          https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat
Used for training and inference of the fine-tuned models.
"""
register_template(
    name="baichuan2",
    prefix=["{{system}}"],
    prompt=[
        {"token": "<reserved_106>"},  # user token
        "{{query}}",
        {"token": "<reserved_107>"},  # assistant token
    ],
    system="",
    sep=[],
)


r"""
Supports: https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat
          https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat
Used for inference of the original model.
"""
register_template(
    name="baichuan2_eval",
    prefix=["{{system}}", {"token": "<reserved_106>"}],  # user token
    prompt=["{{query}}", {"token": "<reserved_107>"}],  # assistant token
    system="",
    sep=[],
    stop_words=["<reserved_106>"],  # user token
)


r"""
Supports: https://huggingface.co/HuggingFaceH4/starchat-alpha
          https://huggingface.co/HuggingFaceH4/starchat-beta

"""
register_template(
    name="starchat",
    prefix=[{"token": "<|system|>"}, "\n{{system}}", {"token": "<|end|>"}],
    prompt=[
        {"token": "<|user|>"},
        "\n{{query}}",
        {"token": "<|end|>"},
        "\n",
        {"token": "<|assistant|>"},
    ],
    system="",
    sep=["\n"],
    stop_words=["<|end|>"],
)


r"""
Supports: https://huggingface.co/Qwen/Qwen-7B-Chat
"""
register_template(
    name="chatml",
    prefix=[{"token": "<|im_start|>"}, "system\n{{system}}", {"token": "<|im_end|>"}],
    prompt=[
        {"token": "<|im_start|>"},
        "user\n{{query}}",
        {"token": "<|im_end|>"},
        "\n",
        {"token": "<|im_start|>"},
        "assistant\n",
    ],
    system="You are a helpful assistant.",
    sep=["\n"],
    stop_words=["<|im_end|>"],
)


r"""
Supports: https://huggingface.co/THUDM/chatglm2-6b
"""
register_template(
    name="chatglm2",
    prefix=[{"token": "[gMASK]"}, {"token": "sop"}, "{{system}}"],
    prompt=["[Round {{idx}}]\n\n问：{{query}}\n\n答："],
    system="",
    sep=["\n\n"],
)


r"""
Supports: https://huggingface.co/xverse/XVERSE-13B-Chat
"""
register_template(
    name="xverse",
    prefix=["{{system}}"],
    prompt=["Human: {{query}}\n\nAssistant: "],
    system="",
    sep=[],
)
