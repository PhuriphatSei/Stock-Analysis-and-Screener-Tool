def dcf_valuation(eps, growth_rate, discount_rate, years=5, terminal_growth=0.02, shares_outstanding=1):
    try:
        cash_flows = []
        current_eps = eps
        for year in range(1, years + 1):
            current_eps *= (1 + growth_rate)
            cash_flows.append(current_eps)

        terminal_value = cash_flows[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)

        discounted_cash_flows = [cf / ((1 + discount_rate) ** i) for i, cf in enumerate(cash_flows, start=1)]
        discounted_terminal_value = terminal_value / ((1 + discount_rate) ** years)

        intrinsic_value = (sum(discounted_cash_flows) + discounted_terminal_value) / shares_outstanding
        return round(intrinsic_value, 2)
    except Exception:
        return None
