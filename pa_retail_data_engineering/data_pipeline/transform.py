from types import SimpleNamespace
from datetime import datetime

class Transformer:
    def __init__(self, extracted_obj):
        self.extracted_obj = extracted_obj
        self.utilities_list = self.transform_data()

    def transform_data(self):
        utilities_list = []
        for item in self.extracted_obj.items: 
            if isinstance(item.utilities, SimpleNamespace):
            # for utility_name, utility_info in item.__dict__.items():
                for utility_name, utility_info in item.utilities.__dict__.items():            
                    utility_data = {'name': utility_name, 'suppliers_data': [], 'rates_data': []}

                    if isinstance(utility_info, SimpleNamespace):
                        utility_info_dict = utility_info.__dict__

                        created_at_str = None

                        if 'default_rate' in utility_info_dict:
                            default_rates = utility_info_dict['default_rate']
                            for rate_info in default_rates:
                                if isinstance(rate_info, SimpleNamespace):
                                    rate_data = {
                                        'min_value': getattr(rate_info, 'min', None),
                                        'max_value': getattr(rate_info, 'max', None),
                                        'rate_type': "default rate",
                                        'amount_data': [],
                                        'createdAt': created_at_str
                                    }
                                    amount = getattr(rate_info, 'amount', None)
                                    if isinstance(amount, (int, float)):
                                        rate_data['amount_data'].append({'value': amount})
                                    elif isinstance(amount, SimpleNamespace):
                                        for day, time_slots in amount.__dict__.items():
                                            for slot in time_slots:
                                                if isinstance(slot, SimpleNamespace):
                                                    rate_data['amount_data'].append({
                                                        'from_value': getattr(slot, 'from', None),
                                                        'to_value': getattr(slot, 'to', None),
                                                        'value': getattr(slot, 'value', None)
                                                    })
                                    elif isinstance(amount, list):
                                        for value in amount:
                                            if isinstance(value, (int, float)):
                                                rate_data['amount_data'].append({'value': value})
                                    utility_data['rates_data'].append(rate_data)

                        if 'default_ra_rate' in utility_info_dict:
                            default_ra_rates = utility_info_dict['default_ra_rate']
                            for rate_info in default_ra_rates:
                                if isinstance(rate_info, SimpleNamespace):
                                    rate_data = {
                                        'min_value': getattr(rate_info, 'min', None),
                                        'max_value': getattr(rate_info, 'max', None),
                                        'rate_type': "default residential add on heat pump service rate",
                                        'amount_data': [],
                                        'createdAt':  created_at_str
                                    }
                                    amount = getattr(rate_info, 'amount', None)
                                    if isinstance(amount, (int, float)):
                                        rate_data['amount_data'].append({'value': amount})
                                    elif isinstance(amount, SimpleNamespace):
                                        for day, time_slots in amount.__dict__.items():
                                            for slot in time_slots:
                                                if isinstance(slot, SimpleNamespace):
                                                    rate_data['amount_data'].append({
                                                        'from_value': getattr(slot, 'from', None),
                                                        'to_value': getattr(slot, 'to', None),
                                                        'value': getattr(slot, 'value', None)
                                                    })
                                    elif isinstance(amount, list):
                                        for value in amount:
                                            if isinstance(value, (int, float)):
                                                rate_data['amount_data'].append({'value': value})
                                    utility_data['rates_data'].append(rate_data)

                        if 'default_rate with_demand_meter' in utility_info_dict:
                            default_rates = utility_info_dict['default_rate with_demand_meter']
                            for rate_info in default_rates:
                                if isinstance(rate_info, SimpleNamespace):
                                    rate_data = {
                                        'min_value': getattr(rate_info, 'min', None),
                                        'max_value': getattr(rate_info, 'max', None),
                                        'rate_type': "default rate with demand meter",
                                        'amount_data': [],
                                        'createdAt':  created_at_str
                                    }
                                    amount = getattr(rate_info, 'amount', None)
                                    if isinstance(amount, (int, float)):
                                        rate_data['amount_data'].append({'value': amount})
                                    elif isinstance(amount, SimpleNamespace):
                                        for day, time_slots in amount.__dict__.items():
                                            for slot in time_slots:
                                                if isinstance(slot, SimpleNamespace):
                                                    rate_data['amount_data'].append({
                                                        'from_value': getattr(slot, 'from', None),
                                                        'to_value': getattr(slot, 'to', None),
                                                        'value': getattr(slot, 'value', None)
                                                    })
                                    elif isinstance(amount, list):
                                        for value in amount:
                                            if isinstance(value, (int, float)):
                                                rate_data['amount_data'].append({'value': value})
                                    utility_data['rates_data'].append(rate_data)

                        if 'default_rate_without_demand_meter' in utility_info_dict:
                            default_rates = utility_info_dict['default_rate_without_demand_meter']
                            for rate_info in default_rates:
                                if isinstance(rate_info, SimpleNamespace):
                                    rate_data = {
                                        'min_value': getattr(rate_info, 'min', None),
                                        'max_value': getattr(rate_info, 'max', None),
                                        'rate_type': "default rate without demand meter",
                                        'amount_data': [],
                                        'createdAt':  created_at_str
                                    }
                                    amount = getattr(rate_info, 'amount', None)
                                    if isinstance(amount, (int, float)):
                                        rate_data['amount_data'].append({'value': amount})
                                    elif isinstance(amount, SimpleNamespace):
                                        for day, time_slots in amount.__dict__.items():
                                            for slot in time_slots:
                                                if isinstance(slot, SimpleNamespace):
                                                    rate_data['amount_data'].append({
                                                        'from_value': getattr(slot, 'from', None),
                                                        'to_value': getattr(slot, 'to', None),
                                                        'value': getattr(slot, 'value', None)
                                                    })
                                    elif isinstance(amount, list):
                                        for value in amount:
                                            if isinstance(value, (int, float)):
                                                rate_data['amount_data'].append({'value': value})
                                    utility_data['rates_data'].append(rate_data)

                        if 'default_rh_rate' in utility_info_dict:
                            default_rh_rates = utility_info_dict['default_rh_rate']
                            for rate_info in default_rh_rates:
                                if isinstance(rate_info, SimpleNamespace):
                                    rate_data = {
                                        'min_value': getattr(rate_info, 'min', None),
                                        'max_value': getattr(rate_info, 'max', None),
                                        'rate_type': "default residential heating rate",
                                        'amount_data': [],
                                        'createdAt':  created_at_str
                                    }
                                    amount = getattr(rate_info, 'amount', None)
                                    if isinstance(amount, (int, float)):
                                        rate_data['amount_data'].append({'value': amount})
                                    elif isinstance(amount, SimpleNamespace):
                                        for day, time_slots in amount.__dict__.items():
                                            for slot in time_slots:
                                                if isinstance(slot, SimpleNamespace):
                                                    rate_data['amount_data'].append({
                                                        'from_value': getattr(slot, 'from', None),
                                                        'to_value': getattr(slot, 'to', None),
                                                        'value': getattr(slot, 'value', None)
                                                    })
                                    elif isinstance(amount, list):
                                        for value in amount:
                                            if isinstance(value, (int, float)):
                                                rate_data['amount_data'].append({'value': value})
                                    utility_data['rates_data'].append(rate_data)

                        if 'suppliers' in utility_info_dict:
                            suppliers = utility_info_dict['suppliers']
                            if isinstance(suppliers, SimpleNamespace):
                                suppliers_dict = suppliers.__dict__
                                for supplier_name, supplier_info in suppliers_dict.items():
                                    supplier_data = {'name': supplier_name, 'plans_data': []}

                                    if isinstance(supplier_info, SimpleNamespace):
                                        supplier_info_dict = supplier_info.__dict__
                                        if 'plans' in supplier_info_dict:
                                            plans = supplier_info_dict['plans']
                                            for plan in plans:
                                                if isinstance(plan, SimpleNamespace):

                                                    created_at_data = getattr(plan, 'created_at', None)
                                                    if created_at_data:
                                                        try:
                                                            created_at_date = datetime(
                                                                year=getattr(created_at_data, "year"),
                                                                month=getattr(created_at_data, "month"),
                                                                day=getattr(created_at_data, "day")
                                                            )
                                                            created_at_str = created_at_date.strftime('%Y-%m-%d')
                                                        except (TypeError, ValueError):
                                                            pass

                                                    start_date_data = getattr(plan, 'start_date', None)
                                                    start_date_str = None
                                                    if start_date_data:
                                                        try:
                                                            start_date = datetime(
                                                                year=getattr(start_date_data, "year"),
                                                                month=getattr(start_date_data, "month"),
                                                                day=getattr(start_date_data, "day")
                                                            )
                                                            start_date_str = start_date.strftime('%Y-%m-%d')
                                                        except (TypeError, ValueError):
                                                            pass

                                                    term_end_date_data = getattr(plan, 'term_end_date', None)
                                                    term_end_date_str = None
                                                    if term_end_date_data:
                                                        try:
                                                            term_end_date = datetime(
                                                                year=getattr(term_end_date_data, "year"),
                                                                month=getattr(term_end_date_data, "month"),
                                                                day=getattr(term_end_date_data, "day")
                                                            )
                                                            term_end_date_str = term_end_date.strftime('%Y-%m-%d')
                                                        except (TypeError, ValueError):
                                                            pass

                                                    plan_end_date_data = getattr(plan, 'plan_end_date', None)
                                                    plan_end_date_str = None
                                                    if plan_end_date_data:
                                                        try:
                                                            plan_end_date = datetime(
                                                                year=getattr(plan_end_date_data, "year"),
                                                                month=getattr(plan_end_date_data, "month"),
                                                                day=getattr(plan_end_date_data, "day")
                                                            )
                                                            plan_end_date_str = plan_end_date.strftime('%Y-%m-%d')
                                                        except (TypeError, ValueError):
                                                            pass

                                                    #rename the utility name to have the actual name:
                                                    if hasattr(plan, 'utility_name'):
                                                        utility_data["name"] = getattr(plan, 'utility_name')

                                                    if hasattr(plan, 'supplier_name'):
                                                        supplier_data["name"] = getattr(plan, 'supplier_name')


                                                    green_value = None
                                                    green_percentage_data = getattr(plan, 'green_percentage', None)
                                                    if  green_percentage_data:
                                                        # Check if green_percentage is a SimpleNamespace object or a direct number
                                                        if isinstance( green_percentage_data, SimpleNamespace):
                                                            green_value = getattr( green_percentage_data, 'amount', None)
                                                        elif isinstance( green_percentage_data, (int, float)):
                                                            green_value =  green_percentage_data

                                                    plan_data = {
                                                        'state': getattr(plan, 'state', None),
                                                        'rate_unit': getattr(plan, 'rate_unit', None),
                                                        'contact_number': getattr(plan, 'contact_number', None),
                                                        'is_variable': getattr(plan, 'is_variable', None),
                                                        'rate_type': getattr(plan, 'rate_type', None),
                                                        'is_green': getattr(plan, 'is_green', None),
                                                        'description': getattr(plan, 'description', None),
                                                        'term': getattr(plan, 'term', None),
                                                        'website_url': getattr(plan, 'website_url', None),
                                                        'green_details': getattr(plan, 'green_details', None),
                                                        'start_date': start_date_str,
                                                        'service_type': getattr(plan, 'service_type', None),
                                                        'term_end_date': term_end_date_str,
                                                        'plan_end_date': plan_end_date_str,
                                                        'sq_ft_2600': getattr(plan, 'sq_ft_2600', None),
                                                        'sq_ft_800': getattr(plan, 'sq_ft_800', None),
                                                        'plan_type': getattr(plan, 'plan_type', None),
                                                        'early_term_fee_data': {},
                                                        'created_at': created_at_str,
                                                        'usage_credits_data': [],
                                                        'rates_data': [],
                                                        'monthly_charges_data': [],
                                                        'benefits_data': [],
                                                        'green_percentage': green_value
                                                    }

                                                    monthly_charges = getattr(plan, 'monthly_charge', [])
                                                    if monthly_charges:
                                                        for monthly_charge in monthly_charges:
                                                            if isinstance(monthly_charge, SimpleNamespace):
                                                                monthly_charge_dict = monthly_charge.__dict__
                                                                monthly_charge_data = {
                                                                    'min_value': getattr(monthly_charge, 'min', None),
                                                                    'max_value': getattr(monthly_charge, 'max', None),
                                                                    'amount_data': []
                                                                }
                                                                amount = getattr(monthly_charge, 'amount', None)
                                                                if isinstance(amount, (int, float)):
                                                                    monthly_charge_data['amount_data'].append({'value': amount})
                                                                elif isinstance(amount, SimpleNamespace):
                                                                    for day, time_slots in amount.__dict__.items():
                                                                        for slot in time_slots:
                                                                            if isinstance(slot, SimpleNamespace):
                                                                                monthly_charge_data['amount_data'].append({
                                                                                    'from_value': getattr(slot, 'from', None),
                                                                                    'to_value': getattr(slot, 'to', None),
                                                                                    'value': getattr(slot, 'value', None)
                                                                                })
                                                                elif isinstance(amount, list):
                                                                    for value in amount:
                                                                        if isinstance(value, (int, float)):
                                                                            monthly_charge_data['amount_data'].append({'value': value})
                                                                plan_data['monthly_charges_data'].append( monthly_charge_data)

                                                    usage_credits = getattr(plan, 'usage_credits', [])
                                                    for credit in usage_credits:
                                                        if isinstance(credit, SimpleNamespace):
                                                            credit_dict = credit.__dict__
                                                            credit_data = {
                                                                'min_value': getattr(credit, 'min', None),
                                                                'max_value': getattr(credit, 'max', None),
                                                                'amount_data': []
                                                            }
                                                            amount = getattr(credit, 'amount', None)
                                                            if isinstance(amount, (int, float)):
                                                                credit_data['amount_data'].append({'value': amount})
                                                            elif isinstance(amount, SimpleNamespace):
                                                                for day, time_slots in amount.__dict__.items():
                                                                    for slot in time_slots:
                                                                        if isinstance(slot, SimpleNamespace):
                                                                            credit_data['amount_data'].append({
                                                                                'from_value': getattr(slot, 'from', None),
                                                                                'to_value': getattr(slot, 'to', None),
                                                                                'value': getattr(slot, 'value', None)
                                                                            })
                                                            elif isinstance(amount, list):
                                                                for value in amount:
                                                                    if isinstance(value, (int, float)):
                                                                        credit_data['amount_data'].append({'value': value})
                                                            plan_data['usage_credits_data'].append(credit_data)

                                                    # Handle early_term_fee
                                                    early_term_fee = getattr(plan, 'early_term_fee', None)
                                                    if early_term_fee:
                                                        # Check if green_percentage is a SimpleNamespace object or a direct number
                                                        if isinstance(early_term_fee, SimpleNamespace):
                                                            # It's a SimpleNamespace object; get its 'type' and 'value'
                                                            early_term_fee_data = {
                                                                'min': getattr(early_term_fee, 'min', None),
                                                                'max': getattr(early_term_fee, 'max', None),
                                                                'early_term_fee_type': getattr(early_term_fee, 'type', None),
                                                                'term': getattr(early_term_fee, 'term', None)
                                                            }
                                                        elif isinstance(early_term_fee, (int, float)):
                                                            # It's a direct number; use it as the 'value' and set 'type' to None or some default
                                                            early_term_fee_data = {
                                                                'min': early_term_fee,
                                                                'max': None,
                                                                'early_term_fee_type': None,
                                                                'term': None
                                                            }
                                                        else:
                                                            # Handle other unexpected formats or set to a default
                                                            early_term_fee_data = {
                                                                'min': None,
                                                                'max': None,
                                                                'early_term_fee_type': None,
                                                                'term': None
                                                            }
                                                        plan_data['early_term_fee_data'] = early_term_fee_data

                                                    # Handle benefits
                                                    benefits = getattr(plan, 'benefit', [])
                                                    if benefits:
                                                        for benefit in benefits:
                                                            if isinstance(benefit, SimpleNamespace):
                                                                benefit_data = {
                                                                    'benefit_type': getattr(benefit, 'type', None),
                                                                    'value': getattr(benefit, 'value', None)
                                                                }
                                                                plan_data['benefits_data'].append(benefit_data)

                                                    rate = getattr(plan, 'rate', [])
                                                    if rate:
                                                        for rate_info in rate:
                                                            if isinstance(rate_info, SimpleNamespace):
                                                                rate_data = {
                                                                    'min_value': getattr(rate_info, 'min', None),
                                                                    'max_value': getattr(rate_info, 'max', None),
                                                                    'rate_type': None,
                                                                    'amount_data': [],
                                                                    'createdAt':created_at_str
                                                                }
                                                                amount = getattr(rate_info, 'amount', None)
                                                                if isinstance(amount, SimpleNamespace):
                                                                    for day, time_slots in amount.__dict__.items():
                                                                        for slot in time_slots:
                                                                            if isinstance(slot, SimpleNamespace):
                                                                                rate_data['amount_data'].append({
                                                                                    'from_value': getattr(slot, 'from', None),
                                                                                    'to_value': getattr(slot, 'to', None),
                                                                                    'value': getattr(slot, 'value', None)
                                                                                })
                                                                elif isinstance(amount, (int, float)):
                                                                    rate_data['amount_data'].append({
                                                                        'from_value': None,
                                                                        'to_value': None,
                                                                        'value': amount
                                                                    })
                                                                plan_data['rates_data'].append(rate_data)
                                                    supplier_data['plans_data'].append(plan_data)
                                    utility_data['suppliers_data'].append(supplier_data)
                    for rate_data in utility_data['rates_data']:
                        rate_data['createdAt'] = created_at_str
                    utilities_list.append(utility_data)
        return utilities_list
# class Transformer: (1999-2013)
#     def __init__(self, extracted_obj):
#         self.extracted_obj = extracted_obj
#         self.utilities_list = self.transform_data()

#     def transform_data(self):
#         utilities_list = []
#         for item in self.extracted_obj.items: 
#             # if isinstance(item.utilities, SimpleNamespace):
#             for utility_name, utility_info in item.__dict__.items():
#                 # for utility_name, utility_info in item.utilities.__dict__.items():            
                    
#                     utility_data = {'name': utility_name, 'suppliers_data': [], 'rates_data': []}

#                     if isinstance(utility_info, SimpleNamespace):
#                         utility_info_dict = utility_info.__dict__

#                         created_at_str = None

#                         if 'default_rate' in utility_info_dict:
#                             default_rates = utility_info_dict['default_rate']
#                             for rate_info in default_rates:
#                                 if isinstance(rate_info, SimpleNamespace):
#                                     rate_data = {
#                                         'min_value': getattr(rate_info, 'min', None),
#                                         'max_value': getattr(rate_info, 'max', None),
#                                         'rate_type': "default rate",
#                                         'amount_data': [],
#                                         'createdAt': created_at_str
#                                     }
#                                     amount = getattr(rate_info, 'amount', None)
#                                     if isinstance(amount, (int, float)):
#                                         rate_data['amount_data'].append({'value': amount})
#                                     elif isinstance(amount, SimpleNamespace):
#                                         for day, time_slots in amount.__dict__.items():
#                                             for slot in time_slots:
#                                                 if isinstance(slot, SimpleNamespace):
#                                                     rate_data['amount_data'].append({
#                                                         'from_value': getattr(slot, 'from', None),
#                                                         'to_value': getattr(slot, 'to', None),
#                                                         'value': getattr(slot, 'value', None)
#                                                     })
#                                     elif isinstance(amount, list):
#                                         for value in amount:
#                                             if isinstance(value, (int, float)):
#                                                 rate_data['amount_data'].append({'value': value})
#                                     utility_data['rates_data'].append(rate_data)

#                         if 'default_ra_rate' in utility_info_dict:
#                             default_ra_rates = utility_info_dict['default_ra_rate']
#                             for rate_info in default_ra_rates:
#                                 if isinstance(rate_info, SimpleNamespace):
#                                     rate_data = {
#                                         'min_value': getattr(rate_info, 'min', None),
#                                         'max_value': getattr(rate_info, 'max', None),
#                                         'rate_type': "default residential add on heat pump service rate",
#                                         'amount_data': [],
#                                         'createdAt':  created_at_str
#                                     }
#                                     amount = getattr(rate_info, 'amount', None)
#                                     if isinstance(amount, (int, float)):
#                                         rate_data['amount_data'].append({'value': amount})
#                                     elif isinstance(amount, SimpleNamespace):
#                                         for day, time_slots in amount.__dict__.items():
#                                             for slot in time_slots:
#                                                 if isinstance(slot, SimpleNamespace):
#                                                     rate_data['amount_data'].append({
#                                                         'from_value': getattr(slot, 'from', None),
#                                                         'to_value': getattr(slot, 'to', None),
#                                                         'value': getattr(slot, 'value', None)
#                                                     })
#                                     elif isinstance(amount, list):
#                                         for value in amount:
#                                             if isinstance(value, (int, float)):
#                                                 rate_data['amount_data'].append({'value': value})
#                                     utility_data['rates_data'].append(rate_data)

#                         if 'default_rate with_demand_meter' in utility_info_dict:
#                             default_rates = utility_info_dict['default_rate with_demand_meter']
#                             for rate_info in default_rates:
#                                 if isinstance(rate_info, SimpleNamespace):
#                                     rate_data = {
#                                         'min_value': getattr(rate_info, 'min', None),
#                                         'max_value': getattr(rate_info, 'max', None),
#                                         'rate_type': "default rate with demand meter",
#                                         'amount_data': [],
#                                         'createdAt':  created_at_str
#                                     }
#                                     amount = getattr(rate_info, 'amount', None)
#                                     if isinstance(amount, (int, float)):
#                                         rate_data['amount_data'].append({'value': amount})
#                                     elif isinstance(amount, SimpleNamespace):
#                                         for day, time_slots in amount.__dict__.items():
#                                             for slot in time_slots:
#                                                 if isinstance(slot, SimpleNamespace):
#                                                     rate_data['amount_data'].append({
#                                                         'from_value': getattr(slot, 'from', None),
#                                                         'to_value': getattr(slot, 'to', None),
#                                                         'value': getattr(slot, 'value', None)
#                                                     })
#                                     elif isinstance(amount, list):
#                                         for value in amount:
#                                             if isinstance(value, (int, float)):
#                                                 rate_data['amount_data'].append({'value': value})
#                                     utility_data['rates_data'].append(rate_data)

#                         if 'default_rate_without_demand_meter' in utility_info_dict:
#                             default_rates = utility_info_dict['default_rate_without_demand_meter']
#                             for rate_info in default_rates:
#                                 if isinstance(rate_info, SimpleNamespace):
#                                     rate_data = {
#                                         'min_value': getattr(rate_info, 'min', None),
#                                         'max_value': getattr(rate_info, 'max', None),
#                                         'rate_type': "default rate without demand meter",
#                                         'amount_data': [],
#                                         'createdAt':  created_at_str
#                                     }
#                                     amount = getattr(rate_info, 'amount', None)
#                                     if isinstance(amount, (int, float)):
#                                         rate_data['amount_data'].append({'value': amount})
#                                     elif isinstance(amount, SimpleNamespace):
#                                         for day, time_slots in amount.__dict__.items():
#                                             for slot in time_slots:
#                                                 if isinstance(slot, SimpleNamespace):
#                                                     rate_data['amount_data'].append({
#                                                         'from_value': getattr(slot, 'from', None),
#                                                         'to_value': getattr(slot, 'to', None),
#                                                         'value': getattr(slot, 'value', None)
#                                                     })
#                                     elif isinstance(amount, list):
#                                         for value in amount:
#                                             if isinstance(value, (int, float)):
#                                                 rate_data['amount_data'].append({'value': value})
#                                     utility_data['rates_data'].append(rate_data)

#                         if 'default_rh_rate' in utility_info_dict:
#                             default_rh_rates = utility_info_dict['default_rh_rate']
#                             for rate_info in default_rh_rates:
#                                 if isinstance(rate_info, SimpleNamespace):
#                                     rate_data = {
#                                         'min_value': getattr(rate_info, 'min', None),
#                                         'max_value': getattr(rate_info, 'max', None),
#                                         'rate_type': "default residential heating rate",
#                                         'amount_data': [],
#                                         'createdAt':  created_at_str
#                                     }
#                                     amount = getattr(rate_info, 'amount', None)
#                                     if isinstance(amount, (int, float)):
#                                         rate_data['amount_data'].append({'value': amount})
#                                     elif isinstance(amount, SimpleNamespace):
#                                         for day, time_slots in amount.__dict__.items():
#                                             for slot in time_slots:
#                                                 if isinstance(slot, SimpleNamespace):
#                                                     rate_data['amount_data'].append({
#                                                         'from_value': getattr(slot, 'from', None),
#                                                         'to_value': getattr(slot, 'to', None),
#                                                         'value': getattr(slot, 'value', None)
#                                                     })
#                                     elif isinstance(amount, list):
#                                         for value in amount:
#                                             if isinstance(value, (int, float)):
#                                                 rate_data['amount_data'].append({'value': value})
#                                     utility_data['rates_data'].append(rate_data)

#                         if 'suppliers' in utility_info_dict:
#                             suppliers = utility_info_dict['suppliers']
#                             if isinstance(suppliers, SimpleNamespace):
#                                 suppliers_dict = suppliers.__dict__
#                                 for supplier_name, supplier_info in suppliers_dict.items():
#                                     supplier_data = {'name': supplier_name, 'plans_data': []}

#                                     if isinstance(supplier_info, SimpleNamespace):
#                                         supplier_info_dict = supplier_info.__dict__
#                                         if 'plans' in supplier_info_dict:
#                                             plans = supplier_info_dict['plans']
#                                             for plan in plans:
#                                                 if isinstance(plan, SimpleNamespace):

#                                                     created_at_data = getattr(plan, 'created_at', None)
#                                                     if created_at_data:
#                                                         try:
#                                                             created_at_date = datetime(
#                                                                 year=getattr(created_at_data, "year"),
#                                                                 month=getattr(created_at_data, "month"),
#                                                                 day=getattr(created_at_data, "day")
#                                                             )
#                                                             created_at_str = created_at_date.strftime('%Y-%m-%d')
#                                                         except (TypeError, ValueError):
#                                                             pass

#                                                     start_date_data = getattr(plan, 'start_date', None)
#                                                     start_date_str = None
#                                                     if start_date_data:
#                                                         try:
#                                                             start_date = datetime(
#                                                                 year=getattr(start_date_data, "year"),
#                                                                 month=getattr(start_date_data, "month"),
#                                                                 day=getattr(start_date_data, "day")
#                                                             )
#                                                             start_date_str = start_date.strftime('%Y-%m-%d')
#                                                         except (TypeError, ValueError):
#                                                             pass

#                                                     term_end_date_data = getattr(plan, 'term_end_date', None)
#                                                     term_end_date_str = None
#                                                     if term_end_date_data:
#                                                         try:
#                                                             term_end_date = datetime(
#                                                                 year=getattr(term_end_date_data, "year"),
#                                                                 month=getattr(term_end_date_data, "month"),
#                                                                 day=getattr(term_end_date_data, "day")
#                                                             )
#                                                             term_end_date_str = term_end_date.strftime('%Y-%m-%d')
#                                                         except (TypeError, ValueError):
#                                                             pass

#                                                     plan_end_date_data = getattr(plan, 'plan_end_date', None)
#                                                     plan_end_date_str = None
#                                                     if plan_end_date_data:
#                                                         try:
#                                                             plan_end_date = datetime(
#                                                                 year=getattr(plan_end_date_data, "year"),
#                                                                 month=getattr(plan_end_date_data, "month"),
#                                                                 day=getattr(plan_end_date_data, "day")
#                                                             )
#                                                             plan_end_date_str = plan_end_date.strftime('%Y-%m-%d')
#                                                         except (TypeError, ValueError):
#                                                             pass

#                                                     #rename the utility name to have the actual name:
#                                                     if hasattr(plan, 'utility_name'):
#                                                         utility_data["name"] = getattr(plan, 'utility_name')

#                                                     if hasattr(plan, 'supplier_name'):
#                                                         supplier_data["name"] = getattr(plan, 'supplier_name')


#                                                     green_value = None
#                                                     green_percentage_data = getattr(plan, 'green_percentage', None)
#                                                     if  green_percentage_data:
#                                                         # Check if green_percentage is a SimpleNamespace object or a direct number
#                                                         if isinstance( green_percentage_data, SimpleNamespace):
#                                                             green_value = getattr( green_percentage_data, 'amount', None)
#                                                         elif isinstance( green_percentage_data, (int, float)):
#                                                             green_value =  green_percentage_data

#                                                     plan_data = {
#                                                         'state': getattr(plan, 'state', None),
#                                                         'rate_unit': getattr(plan, 'rate_unit', None),
#                                                         'contact_number': getattr(plan, 'contact_number', None),
#                                                         'is_variable': getattr(plan, 'is_variable', None),
#                                                         'rate_type': getattr(plan, 'rate_type', None),
#                                                         'is_green': getattr(plan, 'is_green', None),
#                                                         'description': getattr(plan, 'description', None),
#                                                         'term': getattr(plan, 'term', None),
#                                                         'website_url': getattr(plan, 'website_url', None),
#                                                         'green_details': getattr(plan, 'green_details', None),
#                                                         'start_date': start_date_str,
#                                                         'service_type': getattr(plan, 'service_type', None),
#                                                         'term_end_date': term_end_date_str,
#                                                         'plan_end_date': plan_end_date_str,
#                                                         'sq_ft_2600': getattr(plan, 'sq_ft_2600', None),
#                                                         'sq_ft_800': getattr(plan, 'sq_ft_800', None),
#                                                         'plan_type': getattr(plan, 'plan_type', None),
#                                                         'early_term_fee_data': {},
#                                                         'created_at': created_at_str,
#                                                         'usage_credits_data': [],
#                                                         'rates_data': [],
#                                                         'monthly_charges_data': [],
#                                                         'benefits_data': [],
#                                                         'green_percentage': green_value
#                                                     }

#                                                     monthly_charges = getattr(plan, 'monthly_charge', [])
#                                                     if monthly_charges:
#                                                         for monthly_charge in monthly_charges:
#                                                             if isinstance(monthly_charge, SimpleNamespace):
#                                                                 monthly_charge_dict = monthly_charge.__dict__
#                                                                 monthly_charge_data = {
#                                                                     'min_value': getattr(monthly_charge, 'min', None),
#                                                                     'max_value': getattr(monthly_charge, 'max', None),
#                                                                     'amount_data': []
#                                                                 }
#                                                                 amount = getattr(monthly_charge, 'amount', None)
#                                                                 if isinstance(amount, (int, float)):
#                                                                     monthly_charge_data['amount_data'].append({'value': amount})
#                                                                 elif isinstance(amount, SimpleNamespace):
#                                                                     for day, time_slots in amount.__dict__.items():
#                                                                         for slot in time_slots:
#                                                                             if isinstance(slot, SimpleNamespace):
#                                                                                 monthly_charge_data['amount_data'].append({
#                                                                                     'from_value': getattr(slot, 'from', None),
#                                                                                     'to_value': getattr(slot, 'to', None),
#                                                                                     'value': getattr(slot, 'value', None)
#                                                                                 })
#                                                                 elif isinstance(amount, list):
#                                                                     for value in amount:
#                                                                         if isinstance(value, (int, float)):
#                                                                             monthly_charge_data['amount_data'].append({'value': value})
#                                                                 plan_data['monthly_charges_data'].append( monthly_charge_data)

#                                                     usage_credits = getattr(plan, 'usage_credits', [])
#                                                     for credit in usage_credits:
#                                                         if isinstance(credit, SimpleNamespace):
#                                                             credit_dict = credit.__dict__
#                                                             credit_data = {
#                                                                 'min_value': getattr(credit, 'min', None),
#                                                                 'max_value': getattr(credit, 'max', None),
#                                                                 'amount_data': []
#                                                             }
#                                                             amount = getattr(credit, 'amount', None)
#                                                             if isinstance(amount, (int, float)):
#                                                                 credit_data['amount_data'].append({'value': amount})
#                                                             elif isinstance(amount, SimpleNamespace):
#                                                                 for day, time_slots in amount.__dict__.items():
#                                                                     for slot in time_slots:
#                                                                         if isinstance(slot, SimpleNamespace):
#                                                                             credit_data['amount_data'].append({
#                                                                                 'from_value': getattr(slot, 'from', None),
#                                                                                 'to_value': getattr(slot, 'to', None),
#                                                                                 'value': getattr(slot, 'value', None)
#                                                                             })
#                                                             elif isinstance(amount, list):
#                                                                 for value in amount:
#                                                                     if isinstance(value, (int, float)):
#                                                                         credit_data['amount_data'].append({'value': value})
#                                                             plan_data['usage_credits_data'].append(credit_data)

#                                                     # Handle early_term_fee
#                                                     early_term_fee = getattr(plan, 'early_term_fee', None)
#                                                     if early_term_fee:
#                                                         # Check if green_percentage is a SimpleNamespace object or a direct number
#                                                         if isinstance(early_term_fee, SimpleNamespace):
#                                                             # It's a SimpleNamespace object; get its 'type' and 'value'
#                                                             early_term_fee_data = {
#                                                                 'min': getattr(early_term_fee, 'min', None),
#                                                                 'max': getattr(early_term_fee, 'max', None),
#                                                                 'early_term_fee_type': getattr(early_term_fee, 'type', None),
#                                                                 'term': getattr(early_term_fee, 'term', None)
#                                                             }
#                                                         elif isinstance(early_term_fee, (int, float)):
#                                                             # It's a direct number; use it as the 'value' and set 'type' to None or some default
#                                                             early_term_fee_data = {
#                                                                 'min': early_term_fee,
#                                                                 'max': None,
#                                                                 'early_term_fee_type': None,
#                                                                 'term': None
#                                                             }
#                                                         else:
#                                                             # Handle other unexpected formats or set to a default
#                                                             early_term_fee_data = {
#                                                                 'min': None,
#                                                                 'max': None,
#                                                                 'early_term_fee_type': None,
#                                                                 'term': None
#                                                             }
#                                                         plan_data['early_term_fee_data'] = early_term_fee_data

#                                                     # Handle benefits
#                                                     benefits = getattr(plan, 'benefit', [])
#                                                     if benefits:
#                                                         for benefit in benefits:
#                                                             if isinstance(benefit, SimpleNamespace):
#                                                                 benefit_data = {
#                                                                     'benefit_type': getattr(benefit, 'type', None),
#                                                                     'value': getattr(benefit, 'value', None)
#                                                                 }
#                                                                 plan_data['benefits_data'].append(benefit_data)

#                                                     rate = getattr(plan, 'rate', [])
#                                                     if rate:
#                                                         for rate_info in rate:
#                                                             if isinstance(rate_info, SimpleNamespace):
#                                                                 rate_data = {
#                                                                     'min_value': getattr(rate_info, 'min', None),
#                                                                     'max_value': getattr(rate_info, 'max', None),
#                                                                     'rate_type': None,
#                                                                     'amount_data': [],
#                                                                     'createdAt':created_at_str
#                                                                 }
#                                                                 amount = getattr(rate_info, 'amount', None)
#                                                                 if isinstance(amount, SimpleNamespace):
#                                                                     for day, time_slots in amount.__dict__.items():
#                                                                         for slot in time_slots:
#                                                                             if isinstance(slot, SimpleNamespace):
#                                                                                 rate_data['amount_data'].append({
#                                                                                     'from_value': getattr(slot, 'from', None),
#                                                                                     'to_value': getattr(slot, 'to', None),
#                                                                                     'value': getattr(slot, 'value', None)
#                                                                                 })
#                                                                 elif isinstance(amount, (int, float)):
#                                                                     rate_data['amount_data'].append({
#                                                                         'from_value': None,
#                                                                         'to_value': None,
#                                                                         'value': amount
#                                                                     })
#                                                                 plan_data['rates_data'].append(rate_data)
#                                                     supplier_data['plans_data'].append(plan_data)
#                                     utility_data['suppliers_data'].append(supplier_data)
#                     for rate_data in utility_data['rates_data']:
#                         rate_data['createdAt'] = created_at_str
#                     utilities_list.append(utility_data)
#         return utilities_list
        