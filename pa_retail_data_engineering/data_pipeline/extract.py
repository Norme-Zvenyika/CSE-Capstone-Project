from data_pipeline.name_mappings import (
    default_utility_providers_mapping, 
    rate_type_mapping, 
    default_suppliers_names_mapping
)
from datetime import datetime

class Extractor:
    
    def __init__(self):
        pass

    def default_providers_only(self, data):
        
        providers_list = []
        # Iterate through the data (list of utility providers)
        for item in data:
            utility_name = item.get('name', None)
            
            # Correct the provider name using the mapping
            if utility_name:
                utility_name = default_utility_providers_mapping.get(utility_name, utility_name)

            # Check for different types of rates dynamically, each rate type will have its own provider_data
            for rate_type_key in ['default_rate', 'default_rh_rate', 'default_ra_rate', 
                                'default_rate with_demand_meter', 'default_rate_without_demand_meter']:
                if rate_type_key in item:
                    # Extract the rates for the given rate type
                    rates = item[rate_type_key]
                    for rate_info in rates:
                        # Get the created_at date from 'start_date'
                        start_date_info = rate_info.get('start_date', {})
                        created_at_str = None
                        if start_date_info:
                            try:
                                created_at_date = datetime(
                                    year=start_date_info.get('year', None),
                                    month=start_date_info.get('month', None),
                                    day=start_date_info.get('day', None)
                                )
                                created_at_str = created_at_date.strftime('%Y-%m-%d')
                            except (TypeError, ValueError):
                                created_at_str = None

                        # Initialize provider data structure for this rate type
                        provider_data = {
                            'name': utility_name,
                            'suppliers_data': [],
                            'rates_data': []
                        }

                        # Use the mapping to set the standardized rate type name
                        standardized_rate_type = rate_type_mapping.get(rate_type_key, rate_type_key)  # Fallback to original if not mapped

                        for rate_detail in rate_info.get('rate', []):
                            rate_data = {
                                'min_value': rate_detail.get('min', None),
                                'max_value': rate_detail.get('max', None),
                                'rate_type': standardized_rate_type,  # Use the mapped standardized rate type
                                'amount_data': {'value': rate_detail.get('amount', None)},
                                'createdAt': created_at_str
                            }
                            # Append the rate data to the provider
                            provider_data['rates_data'].append(rate_data)

                        # Add provider data for this rate type to the list of providers
                        providers_list.append(provider_data)
        return providers_list

    def process_json_2017_2021(self, data):
        # Initialize an empty list to store all utilities data
        all_utilities_data = []

        # Loop through each element in the data list (assuming it's a list of dictionaries)
        for element in data:
            # Check if the element contains 'utilities'
            if 'utilities' in element:
                utilities = element['utilities']
                
                # Loop through each utility in the 'utilities' dictionary
                for utility_name, utility_info in utilities.items():
                    # Apply utility name mapping
                    mapped_utility_name = default_utility_providers_mapping.get(utility_name, utility_name)

                    # Initialize the utility data structure
                    utility_data = {
                        'name': mapped_utility_name,
                        'suppliers_data': [],
                        'rates_data': []
                    }

                    # Step 1: Handle Suppliers
                    if 'suppliers' in utility_info:
                        suppliers = utility_info['suppliers']

                        for supplier_name, supplier_info in suppliers.items():
                            # Map supplier name using the provided mapping
                            mapped_supplier_name = default_suppliers_names_mapping.get(supplier_name, supplier_name)

                            # Initialize supplier data structure
                            supplier_data = {'name': mapped_supplier_name, 'plans_data': []}

                            # Check for plans under this supplier
                            if 'plans' in supplier_info:
                                plans = supplier_info['plans']

                                for plan in plans:
                                    # Extract plan data as before
                                    created_at_str = None
                                    created_at_data = plan.get('created_at', {})
                                    if created_at_data:
                                        try:
                                            created_at_str = datetime(
                                                year=created_at_data.get('year', None),
                                                month=created_at_data.get('month', None),
                                                day=created_at_data.get('day', None)
                                            ).strftime('%Y-%m-%d')
                                        except (TypeError, ValueError):
                                            created_at_str = None

                                    # Extract other details
                                    start_date_str, term_end_date_str, plan_end_date_str = None, None, None
                                    start_date_data = plan.get('start_date', {})
                                    term_end_date_data = plan.get('term_end_date', {})
                                    plan_end_date_data = plan.get('plan_end_date', {})
                                    try:
                                        if start_date_data:
                                            start_date_str = datetime(
                                                year=start_date_data.get('year', None),
                                                month=start_date_data.get('month', None),
                                                day=start_date_data.get('day', None)
                                            ).strftime('%Y-%m-%d')
                                        if term_end_date_data:
                                            term_end_date_str = datetime(
                                                year=term_end_date_data.get('year', None),
                                                month=term_end_date_data.get('month', None),
                                                day=term_end_date_data.get('day', None)
                                            ).strftime('%Y-%m-%d')
                                        if plan_end_date_data:
                                            plan_end_date_str = datetime(
                                                year=plan_end_date_data.get('year', None),
                                                month=plan_end_date_data.get('month', None),
                                                day=plan_end_date_data.get('day', None)
                                            ).strftime('%Y-%m-%d')
                                    except (TypeError, ValueError):
                                        pass

                                    # Extract green percentage if available
                                    green_percentage_data = plan.get('green_percentage', None)
                                    green_value = None
                                    if isinstance(green_percentage_data, dict):
                                        green_value = green_percentage_data.get('amount', None)
                                    elif isinstance(green_percentage_data, (int, float)):
                                        green_value = green_percentage_data

                                    # Extract plan data
                                    plan_data = {
                                        'state': plan.get('state', None),
                                        'rate_unit': plan.get('rate_unit', None),
                                        'contact_number': plan.get('contact_number', None),
                                        'is_variable': plan.get('is_variable', None),
                                        'rate_type': plan.get('rate_type', None),
                                        'is_green': plan.get('is_green', None),
                                        'description': plan.get('description', None),
                                        'term': plan.get('term', None),
                                        'website_url': plan.get('website_url', None),
                                        'green_details': plan.get('green_details', None),
                                        'start_date': start_date_str,
                                        'service_type': plan.get('service_type', None),
                                        'term_end_date': term_end_date_str,
                                        'plan_end_date': plan_end_date_str,
                                        'sq_ft_2600': plan.get('sq_ft_2600', None),
                                        'sq_ft_800': plan.get('sq_ft_800', None),
                                        'plan_type': plan.get('plan_type', None),
                                        'early_term_fee_data': {},
                                        'created_at': created_at_str,
                                        'usage_credits_data': [],
                                        'rates_data': [],
                                        'monthly_charges_data': [],
                                        'benefits_data': [],
                                        'green_percentage': green_value
                                    }

                                    # Handle rate data for the plan
                                    rate_info_list = plan.get('rate', [])
                                    if isinstance(rate_info_list, list):
                                        for rate_info in rate_info_list:
                                            rate_data = {
                                                'min_value': rate_info.get('min', None),
                                                'max_value': rate_info.get('max', None),
                                                'amount_data': [],  # Initialize empty amount data
                                                'createdAt': created_at_str  # Set createdAt from plan
                                            }
                                            amount = rate_info.get('amount', None)
                                            if isinstance(amount, (int, float)):
                                                rate_data['amount_data'].append({'value': amount})
                                            elif isinstance(amount, dict):  # Handle nested amount structures
                                                for time_slot in amount.values():
                                                    if isinstance(time_slot, dict):
                                                        rate_data['amount_data'].append({
                                                            'from_value': time_slot.get('from', None),
                                                            'to_value': time_slot.get('to', None),
                                                            'value': time_slot.get('value', None)
                                                        })
                                            elif isinstance(amount, list):  # Handle list case
                                                for value in amount:
                                                    if isinstance(value, (int, float)):
                                                        rate_data['amount_data'].append({'value': value})
                                            plan_data['rates_data'].append(rate_data)

                                    # Handle other fields like monthly_charges, usage_credits, etc.
                                    monthly_charges = plan.get('monthly_charge', [])
                                    if isinstance(monthly_charges, list):
                                        for monthly_charge in monthly_charges:
                                            monthly_charge_data = {
                                                'min_value': monthly_charge.get('min', None),
                                                'max_value': monthly_charge.get('max', None),
                                                'amount_data': [{'value': monthly_charge.get('amount', None)}]
                                            }
                                            plan_data['monthly_charges_data'].append(monthly_charge_data)

                                    # Handle usage credits
                                    usage_credits = plan.get('usage_credits', [])
                                    if isinstance(usage_credits, list):
                                        for credit in usage_credits:
                                            credit_data = {
                                                'min_value': credit.get('min', None),
                                                'max_value': credit.get('max', None),
                                                'amount_data': [{'value': credit.get('amount', None)}]
                                            }
                                            plan_data['usage_credits_data'].append(credit_data)

                                    # Handle early_term_fee
                                    early_term_fee = plan.get('early_term_fee', None)
                                    if early_term_fee is not None:
                                        # Check if early_term_fee is a number (int or float)
                                        if isinstance(early_term_fee, (int, float)):
                                            early_term_fee_data = {
                                                'min': early_term_fee,  # Set the early_term_fee directly as 'min'
                                                'max': None,  # No 'max' value in this case
                                                'early_term_fee_type': None,  # No type information
                                                'term': None  # No term information
                                            }
                                        # If early_term_fee is a dictionary-like structure (e.g., SimpleNamespace)
                                        elif isinstance(early_term_fee, dict):
                                            early_term_fee_data = {
                                                'min': early_term_fee.get('min', None),
                                                'max': early_term_fee.get('max', None),
                                                'early_term_fee_type': early_term_fee.get('type', None),
                                                'term': early_term_fee.get('term', None)
                                            }
                                        else:
                                            # Handle any other unexpected formats or set to a default
                                            early_term_fee_data = {
                                                'min': None,
                                                'max': None,
                                                'early_term_fee_type': None,
                                                'term': None
                                            }
                                        # Set the early_term_fee_data in the plan_data
                                        plan_data['early_term_fee_data'] = early_term_fee_data

                                    # Handle benefits
                                    benefits = plan.get('benefit', [])
                                    if isinstance(benefits, list):
                                        for benefit in benefits:
                                            benefit_data = {
                                                'benefit_type': benefit.get('type', None),
                                                'value': benefit.get('value', None)
                                            }
                                            plan_data['benefits_data'].append(benefit_data)

                                    # Add plan details to supplier
                                    supplier_data['plans_data'].append(plan_data)

                            # Add supplier data to the utility
                            utility_data['suppliers_data'].append(supplier_data)

                    # After all rates are processed, set the createdAt for utility rates
                    for rate_data in utility_data['rates_data']:
                        rate_data['CreatedAt'] = created_at_str

                    # Append the utility data to the list of all utilities
                    all_utilities_data.append(utility_data)

        return all_utilities_data
    
    def process_json_2015_2016(self, data):
        # Initialize an empty list to store all utilities data
        all_utilities_data = []
        # Loop through each element in the data list (assuming it's a list of dictionaries)
        for element in data:
            # Check if the element contains 'utilities'
            if 'utilities' in element:
                utilities = element['utilities']
                
                # Loop through each utility in the 'utilities' dictionary
                for utility_name, utility_info in utilities.items():
                    # Apply utility name mapping
                    mapped_utility_name = default_utility_providers_mapping.get(utility_name, utility_name)

                    # Initialize the utility data structure
                    utility_data = {
                        'name': mapped_utility_name,
                        'suppliers_data': [],
                        'rates_data': []
                    }

                    # Step 1: Handle Suppliers
                    if 'suppliers' in utility_info:
                        suppliers = utility_info['suppliers']

                        for supplier_name, supplier_info in suppliers.items():
                            # Map supplier name using the provided mapping
                            mapped_supplier_name = default_suppliers_names_mapping.get(supplier_name, supplier_name)

                            # Initialize supplier data structure
                            supplier_data = {'name': mapped_supplier_name, 'plans_data': []}

                            # Check for plans under this supplier
                            if 'plans' in supplier_info:
                                plans = supplier_info['plans']

                                for plan in plans:
                                    # Extract plan data as before
                                    created_at_str = None
                                    created_at_data = plan.get('created_at', {})
                                    if created_at_data:
                                        try:
                                            created_at_str = datetime(
                                                year=created_at_data.get('year', None),
                                                month=created_at_data.get('month', None),
                                                day=created_at_data.get('day', None)
                                            ).strftime('%Y-%m-%d')
                                        except (TypeError, ValueError):
                                            created_at_str = None

                                    # Extract other details
                                    start_date_str, term_end_date_str, plan_end_date_str = None, None, None
                                    start_date_data = plan.get('start_date', {})
                                    term_end_date_data = plan.get('term_end_date', {})
                                    plan_end_date_data = plan.get('plan_end_date', {})
                                    try:
                                        if start_date_data:
                                            start_date_str = datetime(
                                                year=start_date_data.get('year', None),
                                                month=start_date_data.get('month', None),
                                                day=start_date_data.get('day', None)
                                            ).strftime('%Y-%m-%d')
                                        if term_end_date_data:
                                            term_end_date_str = datetime(
                                                year=term_end_date_data.get('year', None),
                                                month=term_end_date_data.get('month', None),
                                                day=term_end_date_data.get('day', None)
                                            ).strftime('%Y-%m-%d')
                                        if plan_end_date_data:
                                            plan_end_date_str = datetime(
                                                year=plan_end_date_data.get('year', None),
                                                month=plan_end_date_data.get('month', None),
                                                day=plan_end_date_data.get('day', None)
                                            ).strftime('%Y-%m-%d')
                                    except (TypeError, ValueError):
                                        pass

                                    # Extract green percentage if available
                                    green_percentage_data = plan.get('green_percentage', None)
                                    green_value = None
                                    if isinstance(green_percentage_data, dict):
                                        green_value = green_percentage_data.get('amount', None)
                                    elif isinstance(green_percentage_data, (int, float)):
                                        green_value = green_percentage_data

                                    # Extract plan data
                                    plan_data = {
                                        'state': plan.get('state', None),
                                        'rate_unit': plan.get('rate_unit', None),
                                        'contact_number': plan.get('contact_number', None),
                                        'is_variable': plan.get('is_variable', None),
                                        'rate_type': plan.get('rate_type', None),
                                        'is_green': plan.get('is_green', None),
                                        'description': plan.get('description', None),
                                        'term': plan.get('term', None),
                                        'website_url': plan.get('website_url', None),
                                        'green_details': plan.get('green_details', None),
                                        'start_date': start_date_str,
                                        'service_type': plan.get('service_type', None),
                                        'term_end_date': term_end_date_str,
                                        'plan_end_date': plan_end_date_str,
                                        'sq_ft_2600': plan.get('sq_ft_2600', None),
                                        'sq_ft_800': plan.get('sq_ft_800', None),
                                        'plan_type': plan.get('plan_type', None),
                                        'early_term_fee_data': {},
                                        'created_at': created_at_str,
                                        'usage_credits_data': [],
                                        'rates_data': [],
                                        'monthly_charges_data': [],
                                        'benefits_data': [],
                                        'green_percentage': green_value
                                    }

                                    # Handle rate data for the plan
                                    rate_info_list = plan.get('rate', [])
                                    if isinstance(rate_info_list, list):
                                        for rate_info in rate_info_list:
                                            rate_data = {
                                                'min_value': rate_info.get('min', None),
                                                'max_value': rate_info.get('max', None),
                                                'amount_data': [],  # Initialize empty amount data
                                                'createdAt': created_at_str  # Set createdAt from plan
                                            }
                                            amount = rate_info.get('amount', None)
                                            if isinstance(amount, (int, float)):
                                                rate_data['amount_data'].append({'value': amount})
                                            elif isinstance(amount, dict):  # Handle nested amount structures
                                                for time_slot in amount.values():
                                                    rate_data['amount_data'].append({
                                                        'from_value': time_slot.get('from', None),
                                                        'to_value': time_slot.get('to', None),
                                                        'value': time_slot.get('value', None)
                                                    })
                                            plan_data['rates_data'].append(rate_data)

                                    # Handle other fields like monthly_charges, usage_credits, etc.
                                    monthly_charges = plan.get('monthly_charge', [])
                                    if isinstance(monthly_charges, list):
                                        for monthly_charge in monthly_charges:
                                            monthly_charge_data = {
                                                'min_value': monthly_charge.get('min', None),
                                                'max_value': monthly_charge.get('max', None),
                                                'amount_data': [{'value': monthly_charge.get('amount', None)}]
                                            }
                                            plan_data['monthly_charges_data'].append(monthly_charge_data)

                                    # Handle usage credits
                                    usage_credits = plan.get('usage_credits', [])
                                    if isinstance(usage_credits, list):
                                        for credit in usage_credits:
                                            credit_data = {
                                                'min_value': credit.get('min', None),
                                                'max_value': credit.get('max', None),
                                                'amount_data': [{'value': credit.get('amount', None)}]
                                            }
                                            plan_data['usage_credits_data'].append(credit_data)
                                    # Handle early_term_fee
                                    early_term_fee = plan.get('early_term_fee', None)
                                    if early_term_fee is not None:
                                        # Check if early_term_fee is a number (int or float)
                                        if isinstance(early_term_fee, (int, float)):
                                            early_term_fee_data = {
                                                'min': early_term_fee,  # Set the early_term_fee directly as 'min'
                                                'max': None,  # No 'max' value in this case
                                                'early_term_fee_type': None,  # No type information
                                                'term': None  # No term information
                                            }
                                        # If early_term_fee is a dictionary-like structure (e.g., SimpleNamespace)
                                        elif isinstance(early_term_fee, dict):
                                            early_term_fee_data = {
                                                'min': early_term_fee.get('min', None),
                                                'max': early_term_fee.get('max', None),
                                                'early_term_fee_type': early_term_fee.get('type', None),
                                                'term': early_term_fee.get('term', None)
                                            }
                                        else:
                                            # Handle any other unexpected formats or set to a default
                                            early_term_fee_data = {
                                                'min': None,
                                                'max': None,
                                                'early_term_fee_type': None,
                                                'term': None
                                            }
                                        # Set the early_term_fee_data in the plan_data
                                        plan_data['early_term_fee_data'] = early_term_fee_data

                                    # Handle benefits
                                    benefits = plan.get('benefit', [])
                                    if isinstance(benefits, list):
                                        for benefit in benefits:
                                            benefit_data = {
                                                'benefit_type': benefit.get('type', None),
                                                'value': benefit.get('value', None)
                                            }
                                            plan_data['benefits_data'].append(benefit_data)

                                    # Add plan details to supplier
                                    supplier_data['plans_data'].append(plan_data)

                            # Add supplier data to the utility
                            utility_data['suppliers_data'].append(supplier_data)

                    # After all rates are processed, set the createdAt for utility rates
                    for rate_data in utility_data['rates_data']:
                        rate_data['CreatedAt'] = created_at_str

                    # Append the utility data to the list of all utilities
                    all_utilities_data.append(utility_data)

        return all_utilities_data


    def process_json_1999_2013(self, data):
        """
        Process the JSON data specifically for years 1999-2013.
        """
        # Initialize an empty list to store all utilities data
        all_utilities_data = []
        
        # Loop through each utility in the data
        for utility in data:
            # Get the utility name (first key in each object)
            utility_name = list(utility.keys())[0]

            # Apply utility name mapping
            mapped_utility_name = default_utility_providers_mapping.get(utility_name, utility_name)

            # Initialize the utility data structure
            utility_data = {
                'name': mapped_utility_name,
                'suppliers_data': [],
                'rates_data': []
            }

            # Fetch utility info (default rates and suppliers)
            utility_info = utility[utility_name]
            
            # Step 1: Handle Default Rates (with rate type mapping)
            created_at_str = None  # Initialize createdAt as None

            for rate_type_key in ['default_rate', 'default_rh_rate', 'default_ra_rate', 'default_rate with_demand_meter', 'default_rate_without_demand_meter']:
                if rate_type_key in utility_info:
                    default_rates = utility_info[rate_type_key]

                    # Ensure it's a list of rate data
                    if isinstance(default_rates, list):
                        for rate_info in default_rates:
                            rate_data = {
                                'min_value': rate_info.get('min', None),
                                'max_value': rate_info.get('max', None),
                                'rate_type': rate_type_mapping.get(rate_type_key, rate_type_key),  # Map to human-readable rate type
                                'amount_data': [],  # Initialize empty amount data
                                'createdAt': created_at_str  # Set initially to None
                            }
                            # Handle the amount field and nested structures
                            amount = rate_info.get('amount', None)
                            if isinstance(amount, (int, float)):  # If it's a number
                                rate_data['amount_data'].append({'value': amount})
                            elif isinstance(amount, dict):  # If it's a nested structure (like time slots)
                                for time_slot in amount.values():
                                    rate_data['amount_data'].append({
                                        'from_value': time_slot.get('from', None),
                                        'to_value': time_slot.get('to', None),
                                        'value': time_slot.get('value', None)
                                    })

                            # Append the rate data to utility data
                            utility_data['rates_data'].append(rate_data)

            # Step 2: Handle Suppliers
            if 'suppliers' in utility_info:
                suppliers = utility_info['suppliers']
                
                for supplier_name, supplier_info in suppliers.items():
                    # Map supplier name using the provided mapping
                    mapped_supplier_name = default_suppliers_names_mapping.get(supplier_name, supplier_name)
                    
                    # Initialize supplier data structure
                    supplier_data = {'name': mapped_supplier_name, 'plans_data': []}
                    
                    # Check for plans under this supplier
                    if 'plans' in supplier_info:
                        plans = supplier_info['plans']
                        
                        for plan in plans:
                            # Extract all required details from the plan
                            created_at_str = None  # Reset createdAt for each plan
                            
                            # Handle plan's created_at if available
                            created_at_data = plan.get('created_at', {})
                            if created_at_data:
                                try:
                                    created_at_str = datetime(
                                        year=created_at_data.get('year', None),
                                        month=created_at_data.get('month', None),
                                        day=created_at_data.get('day', None)
                                    ).strftime('%Y-%m-%d')
                                except (TypeError, ValueError):
                                    created_at_str = None
                            
                            # Extract start, term_end, and plan_end dates
                            start_date_str, term_end_date_str, plan_end_date_str = None, None, None
                            start_date_data = plan.get('start_date', {})
                            term_end_date_data = plan.get('term_end_date', {})
                            plan_end_date_data = plan.get('plan_end_date', {})
                            try:
                                if start_date_data:
                                    start_date_str = datetime(
                                        year=start_date_data.get('year', None),
                                        month=start_date_data.get('month', None),
                                        day=start_date_data.get('day', None)
                                    ).strftime('%Y-%m-%d')
                                if term_end_date_data:
                                    term_end_date_str = datetime(
                                        year=term_end_date_data.get('year', None),
                                        month=term_end_date_data.get('month', None),
                                        day=term_end_date_data.get('day', None)
                                    ).strftime('%Y-%m-%d')
                                if plan_end_date_data:
                                    plan_end_date_str = datetime(
                                        year=plan_end_date_data.get('year', None),
                                        month=plan_end_date_data.get('month', None),
                                        day=plan_end_date_data.get('day', None)
                                    ).strftime('%Y-%m-%d')
                            except (TypeError, ValueError):
                                pass
                            
                            # Extract green percentage if available
                            green_percentage_data = plan.get('green_percentage', None)
                            green_value = None
                            if isinstance(green_percentage_data, dict):
                                green_value = green_percentage_data.get('amount', None)
                            elif isinstance(green_percentage_data, (int, float)):
                                green_value = green_percentage_data
                            

                            # Extract plan data
                            plan_data = {
                                'state': plan.get('state', None),
                                'rate_unit': plan.get('rate_unit', None),
                                'contact_number': plan.get('plan_phone', None),
                                'is_variable': plan.get('is_variable', None),
                                'rate_type': plan.get('rate_type', None),
                                'is_green': plan.get('is_green', None),
                                'description': plan.get('description', None),
                                'term': plan.get('term', None),
                                'website_url': plan.get('website_url', None),
                                'green_details': plan.get('green_details', None),
                                'start_date': start_date_str,
                                'service_type': plan.get('service_type', None),
                                'term_end_date': term_end_date_str,
                                'plan_end_date': plan_end_date_str,
                                'sq_ft_2600': plan.get('sq_ft_2600', None),
                                'sq_ft_800': plan.get('sq_ft_800', None),
                                'plan_type': plan.get('plan_type', None),
                                'early_term_fee_data': {},
                                'created_at': created_at_str,
                                'usage_credits_data': [],
                                'rates_data': [],
                                'monthly_charges_data': [],
                                'benefits_data': [],
                                'green_percentage': green_value
                            }

                            # Handle rate data for the plan
                            rate_info_list = plan.get('rate', [])
                            if isinstance(rate_info_list, list):
                                for rate_info in rate_info_list:
                                    rate_data = {
                                        'min_value': rate_info.get('min', None),
                                        'max_value': rate_info.get('max', None),
                                        'amount_data': [],  # Initialize empty amount data
                                        'createdAt': created_at_str  # Set createdAt from plan
                                    }
                                    amount = rate_info.get('amount', None)
                                    if isinstance(amount, (int, float)):
                                        rate_data['amount_data'].append({'value': amount})
                                    elif isinstance(amount, dict):  # Handle nested amount structures
                                        for time_slot in amount.values():
                                            rate_data['amount_data'].append({
                                                'from_value': time_slot.get('from', None),
                                                'to_value': time_slot.get('to', None),
                                                'value': time_slot.get('value', None)
                                            })
                                    plan_data['rates_data'].append(rate_data)

                            # Handle other fields like monthly_charges, usage_credits, etc.
                            monthly_charges = plan.get('monthly_charge', [])
                            if isinstance(monthly_charges, list):
                                for monthly_charge in monthly_charges:
                                    monthly_charge_data = {
                                        'min_value': monthly_charge.get('min', None),
                                        'max_value': monthly_charge.get('max', None),
                                        'amount_data': [{'value': monthly_charge.get('amount', None)}]
                                    }
                                    plan_data['monthly_charges_data'].append(monthly_charge_data)

                            # Handle usage credits
                            usage_credits = plan.get('usage_credits', [])
                            if isinstance(usage_credits, list):
                                for credit in usage_credits:
                                    credit_data = {
                                        'min_value': credit.get('min', None),
                                        'max_value': credit.get('max', None),
                                        'amount_data': [{'value': credit.get('amount', None)}]
                                    }
                                    plan_data['usage_credits_data'].append(credit_data)

                            # Handle benefits
                            benefits = plan.get('benefit', [])
                            if isinstance(benefits, list):
                                for benefit in benefits:
                                    benefit_data = {
                                        'benefit_type': benefit.get('type', None),
                                        'value': benefit.get('value', None)
                                    }
                                    plan_data['benefits_data'].append(benefit_data)


                            # Handle early_term_fee
                            early_term_fee = plan.get('early_term_fee', None)
                            if early_term_fee is not None:
                                # Check if early_term_fee is a number (int or float)
                                if isinstance(early_term_fee, (int, float)):
                                    early_term_fee_data = {
                                        'min': early_term_fee,  # Set the early_term_fee directly as 'min'
                                        'max': None,  # No 'max' value in this case
                                        'early_term_fee_type': None,  # No type information
                                        'term': None  # No term information
                                    }
                                # If early_term_fee is a dictionary-like structure (e.g., SimpleNamespace)
                                elif isinstance(early_term_fee, dict):
                                    early_term_fee_data = {
                                        'min': early_term_fee.get('min', None),
                                        'max': early_term_fee.get('max', None),
                                        'early_term_fee_type': early_term_fee.get('type', None),
                                        'term': early_term_fee.get('term', None)
                                    }
                                else:
                                    # Handle any other unexpected formats or set to a default
                                    early_term_fee_data = {
                                        'min': None,
                                        'max': None,
                                        'early_term_fee_type': None,
                                        'term': None
                                    }
                                # Set the early_term_fee_data in the plan_data
                                plan_data['early_term_fee_data'] = early_term_fee_data

                            # Add plan details to supplier
                            supplier_data['plans_data'].append(plan_data)
                    
                    # Add supplier data to the utility
                    utility_data['suppliers_data'].append(supplier_data)

            # After all rates are processed, set the createdAt for utility rates
            for rate_data in utility_data['rates_data']:
                rate_data['createdAt'] = created_at_str

            # Append the utility data to the list of all utilities
            all_utilities_data.append(utility_data)

            return all_utilities_data

