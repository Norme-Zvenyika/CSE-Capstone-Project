import csv
import os

class Loader:
    def __init__(self, model_obj):
        self.model_obj = model_obj
        self.files = {}
        self.id_counters = {}
        self.name_to_id = {
            'utilities': {},
            'suppliers': {}
        }
        self.setup_csv_files()
        self.load()
        self.close_files()

    def setup_csv_files(self):
        tables = ['utilities', 'rates', 'amounts', 'suppliers', 'plans', 'monthly_charges', 'usage_credits', 'early_term_fees', 'benefits']
        headers = {
            'utilities': ['id', 'name'],
            'rates': ['id', 'rate_type', 'min_value', 'max_value', 'utility_id', 'plan_id', 'createdAt'],
            'amounts': ['id', 'from_value', 'to_value', 'value', 'rate_id','usage_credit_id','monthly_charge_id'],
            'suppliers': ['id', 'name', 'utility_id'],
            'plans': ['id', 'created_at', 'state', 'rate_unit', 'contact_number', 'is_variable', 'rate_type', 'is_green', 'description', 'term', 'website_url', 'green_details', 'green_percentage', 'start_date', 'service_type', 'term_end_date', 'plan_end_date', 'sq_ft_2600', 'sq_ft_800', 'plan_type', 'supplier_id'],
            'monthly_charges': ['id', 'min_value', 'max_value', 'plan_id'],
            'usage_credits': ['id', 'min_value', 'max_value', 'plan_id'],
            'early_term_fees': ['id', 'min_value', 'max_value', 'fee_type', 'term', 'plan_id'],
            'benefits': ['id', 'benefit_type', 'value', 'plan_id']
        }
        for table in tables:
            file_path = f'{table}.csv'
            file_exists = os.path.exists(file_path)
            self.files[table] = open(file_path, 'a+', newline='', encoding='utf-8')
            if not file_exists:
                writer = csv.writer(self.files[table])
                writer.writerow(headers[table])
                self.id_counters[table] = 1  
            else:
                self.files[table].seek(0)
                reader = csv.DictReader(self.files[table])
                max_id = 0
                for row in reader:
                    if table == 'utilities' or table == 'suppliers':
                        self.name_to_id[table][row['name']] = int(row['id'])
                    max_id = max(max_id, int(row['id']))
                self.id_counters[table] = max_id + 1
                self.files[table].seek(0, os.SEEK_END) 

    def get_next_id(self, table_name):
        current_id = self.id_counters[table_name]
        self.id_counters[table_name] += 1
        return current_id

    def write_to_csv(self, table_name, data):
        writer = csv.writer(self.files[table_name])
        writer.writerow(data)

    def close_files(self):
        for file in self.files.values():
            file.close()

    def load(self):
        for utility in self.model_obj.utilities:
            if utility.name in self.name_to_id['utilities']:
                utility_id = self.name_to_id['utilities'][utility.name]
            else:
                utility_id = self.get_next_id('utilities')
                self.write_to_csv('utilities', [utility_id, utility.name])
                self.name_to_id['utilities'][utility.name] = utility_id

            for rate in utility.rates:
                rate_id = self.get_next_id('rates')
                self.write_to_csv('rates', [rate_id, rate.rate_type, rate.min_value, rate.max_value, utility_id, None, rate.rate_createdAt])

                for amount in rate.amounts:
                    amount_id = self.get_next_id('amounts')
                    self.write_to_csv('amounts', [amount_id, amount.from_value, amount.to_value, amount.value, rate_id, None, None])

            for supplier in utility.suppliers:
                if supplier.name in self.name_to_id['suppliers']:
                    supplier_id = self.name_to_id['suppliers'][supplier.name]
                else:
                    supplier_id = self.get_next_id('suppliers')
                    self.write_to_csv('suppliers', [supplier_id, supplier.name, utility_id])
                    self.name_to_id['suppliers'][supplier.name] = supplier_id

                for plan in supplier.plans:
                    plan_id = self.get_next_id('plans')
                    plan_data = [plan_id, plan.created_at, plan.state, plan.rate_unit, plan.contact_number, plan.is_variable, plan.rate_type, plan.is_green, plan.description, plan.term, plan.website_url, plan.green_details, plan.green_percentage, plan.start_date, plan.service_type, plan.term_end_date, plan.plan_end_date, plan.sq_ft_2600, plan.sq_ft_800, plan.plan_type, supplier_id]
                    self.write_to_csv('plans', plan_data)

                    for rate in plan.rates:
                        rate_id = self.get_next_id('rates')
                        self.write_to_csv('rates', [rate_id, rate.rate_type, rate.min_value, rate.max_value, None , plan_id, rate.rate_createdAt])
                        for amount in rate.amounts:
                            amount_id = self.get_next_id('amounts')
                            self.write_to_csv('amounts', [amount_id, amount.from_value, amount.to_value, amount.value, rate_id, None,None])

                    for monthly_charge in plan.monthly_charges:
                        monthly_charge_id = self.get_next_id('monthly_charges')
                        self.write_to_csv('monthly_charges', [monthly_charge_id, monthly_charge.min_value, monthly_charge.max_value, plan_id])

                        for amount in monthly_charge.amounts:
                            amount_id = self.get_next_id('amounts')
                            self.write_to_csv('amounts', [amount_id, amount.from_value, amount.to_value, amount.value, None, None, monthly_charge_id])

                    for usage_credit in plan.usage_credits:
                        usage_credit_id = self.get_next_id('usage_credits')
                        self.write_to_csv('usage_credits', [usage_credit_id, usage_credit.min_value, usage_credit.max_value, plan_id])

                        for amount in usage_credit.amounts:
                            amount_id = self.get_next_id('amounts')
                            self.write_to_csv('amounts', [amount_id, amount.from_value, amount.to_value, amount.value, None, usage_credit_id, None])

                    if plan.early_term_fee and plan.early_term_fee.min is not None:
                        early_term_fee_id = self.get_next_id('early_term_fees')
                        early_term_fee_data = [early_term_fee_id, plan.early_term_fee.min, plan.early_term_fee.max, plan.early_term_fee.early_term_fee_type, plan.early_term_fee.term, plan_id]
                        self.write_to_csv('early_term_fees', early_term_fee_data)

                    for benefit in plan.benefits:
                        benefit_id = self.get_next_id('benefits')
                        benefit_data = [benefit_id, benefit.benefit_type, benefit.value, plan_id]
                        self.write_to_csv('benefits', benefit_data)
