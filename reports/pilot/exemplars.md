# Pilot exemplar close-reads

Three sentences read with the human receipts. Picked mechanically from pooled model spread vs retained human spread — see criteria per section.

## model_pins_on_coinflip — NZ-006 (mid-split)

> The first three years of the coming National Government will be very largely devoted to restoring New Zealand's shattered economy.

- master (gold): 408 | section: THE ECONOMY
- human FULL (23 coders): {'408': 11, '404': 5, '305': 4, '414': 1, '412': 1, '303': 1}
- human RETAINED (12 coders): {'408': 6, '305': 3, '404': 2, '414': 1}
- model POOLED spread: 1-modal=0.01, Hnorm=0.01, modal=408
    - anthropic__claude-3.5-haiku__off: {'408': 10}
    - anthropic__claude-haiku-4.5__off: {'408': 10}
    - anthropic__claude-haiku-4.5__on: {'408': 10}
    - deepseek__deepseek-v4-flash__off: {'408': 9, '414': 1}
    - deepseek__deepseek-v4-flash__on: {'408': 10}
    - deepseek__deepseek-v4-pro__on: {'408': 10}
    - google__gemma-4-26b-a4b-it__off: {'408': 10}
    - google__gemma-4-26b-a4b-it__on: {'408': 10}
    - google__gemma-4-31b-it__off: {'408': 10}
    - google__gemma-4-31b-it__on: {'408': 10}
    - qwen__qwen3.6-35b-a3b__off: {'408': 10}
    - qwen__qwen3.6-35b-a3b__on: {'408': 10}
    - qwen__qwen3.6-plus__off: {'408': 10}
    - qwen__qwen3.6-plus__on: {'408': 10}

## both_waver — GB-033 (high-split)

> Much of the present unemployment is a direct result of the civil war in British industry, of restrictive practices and low investment.

- master (gold): 408 | section: THE IMMEDIATE CRISIS: JOBS AND PRICES
- human FULL (32 coders): {'405': 5, '408': 4, '401': 3, '407': 3, '410': 3, '403': 2, '409': 2, '402': 2, '305': 2, '411': 1, '701': 1, '000': 1, '304': 1, '414': 1, '404': 1}
- human RETAINED (17 coders): {'405': 4, '408': 3, '407': 2, '410': 2, '401': 1, '409': 1, '701': 1, '402': 1, '403': 1, '305': 1}
- model POOLED spread: 1-modal=0.69, Hnorm=0.43, modal=702
    - anthropic__claude-3.5-haiku__off: {'701': 4, '401': 1, '403': 1, '703': 1, '705': 1, '405': 1, '402': 1}
    - anthropic__claude-haiku-4.5__off: {'702': 10}
    - anthropic__claude-haiku-4.5__on: {'408': 4, '702': 4, '403': 1, '410': 1}
    - deepseek__deepseek-v4-flash__off: {'703': 4, '503': 1, '403': 1, '702': 1, '502': 1, '305': 1, '607': 1}
    - deepseek__deepseek-v4-flash__on: {'702': 10}
    - deepseek__deepseek-v4-pro__on: {'606': 6, '408': 4}
    - google__gemma-4-26b-a4b-it__off: {'410': 10}
    - google__gemma-4-26b-a4b-it__on: {'702': 7, 'OFF': 3}
    - google__gemma-4-31b-it__off: {'408': 10}
    - google__gemma-4-31b-it__on: {'408': 7, 'OFF': 3}
    - qwen__qwen3.6-35b-a3b__off: {'409': 3, '410': 2, '701': 1, '408': 1, '305': 1, '403': 1, '506': 1}
    - qwen__qwen3.6-35b-a3b__on: {'702': 8, '408': 2}
    - qwen__qwen3.6-plus__off: {'408': 3, '702': 2, '305': 1, '701': 1, '401': 1, '503': 1, '606': 1}
    - qwen__qwen3.6-plus__on: {'408': 5, '410': 3, '702': 1, '405': 1}

## alien_confusion — GB-016 (high-split)

> Rundown cities and declining rural services alike tell a story of a warped sense of priorities by successive governments.

- master (gold): 606 | section: Working together for Britain
- human FULL (32 coders): {'606': 8, '305': 7, '411': 3, '504': 3, '602': 3, '000': 2, '304': 1, '605': 1, '407': 1, '601': 1, '703': 1, '301': 1}
- human RETAINED (17 coders): {'606': 7, '305': 4, '504': 2, '411': 2, '605': 1, '407': 1}
- model POOLED spread: 1-modal=0.81, Hnorm=0.46, modal=303
    - anthropic__claude-3.5-haiku__off: {'301': 4, '503': 3, '504': 1, '505': 1, '606': 1}
    - anthropic__claude-haiku-4.5__off: {'301': 7, '606': 3}
    - anthropic__claude-haiku-4.5__on: {'606': 3, '504': 2, '305': 2, '411': 1, '301': 1, '303': 1}
    - deepseek__deepseek-v4-flash__off: {'503': 9, '504': 1}
    - deepseek__deepseek-v4-flash__on: {'303': 6, '305': 2, '503': 1, '504': 1}
    - deepseek__deepseek-v4-pro__on: {'OFF': 4, '606': 2, '305': 2, '504': 1, '503': 1}
    - google__gemma-4-26b-a4b-it__off: {'303': 10}
    - google__gemma-4-26b-a4b-it__on: {'OFF': 8, '305': 2}
    - google__gemma-4-31b-it__off: {'303': 6, '408': 3, '504': 1}
    - google__gemma-4-31b-it__on: {'OFF': 8, '303': 1, '504': 1}
    - qwen__qwen3.6-35b-a3b__off: {'606': 3, '505': 2, '602': 1, '601': 1, '303': 1, '000': 1, '506': 1}
    - qwen__qwen3.6-35b-a3b__on: {'OFF': 5, '303': 1, '606': 1, '411': 1, '505': 1, '504': 1}
    - qwen__qwen3.6-plus__off: {'305': 3, '505': 2, '504': 2, '408': 2, '000': 1}
    - qwen__qwen3.6-plus__on: {'305': 5, '504': 2, '303': 1, '408': 1, '606': 1}
