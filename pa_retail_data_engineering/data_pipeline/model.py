class EarlyTermFee:
    def __init__(self, min=None, max=None, early_term_fee_type=None, term=None):
        self.min = min
        self.max = max
        self.early_term_fee_type = early_term_fee_type
        self.term = term

class MonthlyCharge:
    def __init__(self, min_value=None, max_value=None, amount_data=None):
        self.min_value = min_value
        self.max_value = max_value
        if isinstance(amount_data, list):
            self.amounts = [Amount(**data) for data in amount_data]
        elif isinstance(amount_data, dict):
            self.amounts = Amount(**amount_data)
        else:
            self.amounts = None

class Benefit:
    def __init__(self, benefit_type=None, value=None):
        self.benefit_type = benefit_type
        self.value = value

class Amount:
    def __init__(self, from_value=None, to_value=None, value=None):
        self.from_value = from_value
        self.to_value = to_value
        self.value = value

class Rate:
    def __init__(self, min_value=None, max_value=None, rate_type=None, amount_data=None, createdAt=None):
        self.min_value = min_value
        self.max_value = max_value
        self.rate_type = rate_type
        self.rate_createdAt = createdAt
        if isinstance(amount_data, list):
            self.amounts = [Amount(**data) for data in amount_data]
        elif isinstance(amount_data, dict):
            self.amounts = [Amount(**amount_data)]
        elif isinstance(amount_data, (int, float)):
            self.amounts = [Amount(value=amount_data)]
        else:
            self.amounts = []

class UsageCredits:
    def __init__(self, min_value=None, max_value=None, amount_data=None):
        self.min_value = min_value
        self.max_value = max_value
        if isinstance(amount_data, list):
            self.amounts = [Amount(**data) for data in amount_data]
        elif isinstance(amount_data, dict):
            self.amounts = [Amount(**amount_data)]
        else:
            self.amounts = []

class Plan:
    def __init__(self, state=None, rate_unit=None, contact_number=None,
                 is_variable=None, rate_type=None, is_green=None, description=None,
                 term=None, website_url=None, green_percentage=None, start_date=None, service_type=None,
                 term_end_date=None, plan_end_date=None, sq_ft_2600=None, sq_ft_800=None,
                 plan_type=None, monthly_charges_data=None, usage_credits_data=None,
                 rates_data=None, green_details=None,
                 benefits_data=None,created_at=None, early_term_fee_data=None):
        self.state = state
        self.rate_unit = rate_unit
        self.contact_number = contact_number
        self.is_variable = is_variable
        self.rate_type = rate_type
        self.is_green = is_green
        self.description = description
        self.term = term
        self.early_term_fee = EarlyTermFee(**(early_term_fee_data or {}))
        self.website_url = website_url
        self.green_details = green_details
        self.green_percentage = green_percentage
        self.start_date = start_date
        self.service_type = service_type
        self.term_end_date = term_end_date
        self.plan_end_date = plan_end_date
        self.sq_ft_2600 = sq_ft_2600
        self.sq_ft_800 = sq_ft_800
        self.plan_type = plan_type
        self.monthly_charges = [MonthlyCharge(**mc) for mc in (monthly_charges_data or [])]
        self.usage_credits = [UsageCredits(**uc) for uc in (usage_credits_data or [])]
        self.rates = [Rate(**r) for r in (rates_data or [])]
        self.benefits = [Benefit(**benefit) for benefit in (benefits_data or [])]
        self.created_at = created_at

class Supplier:
    def __init__(self, name=None, plans_data=None):
        self.name = name
        self.plans = [Plan(**plan) for plan in (plans_data or [])]

class Utility:
    def __init__(self, name=None,suppliers_data=None, rates_data=None):
        self.name = name
        self.rates = [Rate(**rate) for rate in (rates_data or [])]
        self.suppliers = [Supplier(**supplier) for supplier in (suppliers_data or [])]

class Model:
    def __init__(self, utilities_data=None):
        self.utilities = [Utility(**utility) for utility in (utilities_data or [])]
