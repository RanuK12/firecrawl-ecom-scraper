    # If after all processing the price is empty, just '-' (a dash), or non-numeric, return empty string
    if not price_clean or price_clean in ('-', '--', '-.', '.-') or not re.search(r'\d', price_clean):
        price_clean = ''
