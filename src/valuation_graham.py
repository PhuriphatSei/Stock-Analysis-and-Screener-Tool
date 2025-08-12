def graham_valuation(eps, book_value_per_share, growth_rate=5, bond_yield=4.4):
    """
    คำนวณ Graham Number จาก EPS และ Book Value per Share
    """
    try:
        intrinsic_value = (eps * (8.5 + 2 * growth_rate) * bond_yield) / 4.4
        return round(intrinsic_value, 2)
    except Exception:
        return None
