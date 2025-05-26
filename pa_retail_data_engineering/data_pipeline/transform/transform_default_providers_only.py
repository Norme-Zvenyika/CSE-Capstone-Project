"""
Transforms raw JSON records from the default providers-only query
into the normalized utility-supplier-plan structure expected by the load stage.
"""

from datetime import datetime
from .base import (
    BaseTransform,
    default_utility_providers_mapping,
    rate_type_mapping,
)


class TransformDefaultProvidersOnly(BaseTransform):
    """handles JSON from the defaul providers only query"""

    def transform(self, data):

        providers_list = []
        # Iterate through the data (list of utility providers)
        for item in data:
            utility_name = item.get("name", None)

            # Correct the provider name using the mapping
            if utility_name:
                utility_name = default_utility_providers_mapping.get(
                    utility_name, utility_name
                )

            # Check for different types of rates dynamically
            for rate_type_key in [
                "default_rate",
                "default_rh_rate",
                "default_ra_rate",
                "default_rate with_demand_meter",
                "default_rate_without_demand_meter",
            ]:
                if rate_type_key in item:
                    # Extract the rates for the given rate type
                    rates = item[rate_type_key]
                    for rate_info in rates:
                        # Get the created_at date from 'start_date'
                        start_date_info = rate_info.get("start_date", {})
                        created_at_str = None
                        if start_date_info:
                            try:
                                created_at_date = datetime(
                                    year=start_date_info.get("year", None),
                                    month=start_date_info.get("month", None),
                                    day=start_date_info.get("day", None),
                                )
                                created_at_str = created_at_date.strftime("%Y-%m-%d")
                            except (TypeError, ValueError):
                                created_at_str = None

                        # Initialize provider data structure for this rate type
                        provider_data = {
                            "name": utility_name,
                            "suppliers_data": [],
                            "rates_data": [],
                        }

                        # Use the mapping to set the standardized rate type name
                        standardized_rate_type = rate_type_mapping.get(
                            rate_type_key, rate_type_key
                        )  # Fallback to original if not mapped

                        for rate_detail in rate_info.get("rate", []):
                            rate_data = {
                                "min_value": rate_detail.get("min", None),
                                "max_value": rate_detail.get("max", None),
                                "rate_type": standardized_rate_type,
                                "amount_data": {
                                    "value": rate_detail.get("amount", None)
                                },
                                "createdAt": created_at_str,
                            }
                            # Append the rate data to the provider
                            provider_data["rates_data"].append(rate_data)

                        # Add provider data for this rate type to the list of providers
                        providers_list.append(provider_data)
        return providers_list
