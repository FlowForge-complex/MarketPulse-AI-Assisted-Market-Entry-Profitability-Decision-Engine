"""Bottom-up Total Addressable Market (TAM) Guesstimation Engine."""

from typing import Optional

from src.core.logging_config import get_logger
from src.core.types import TAMParameters, TAMResult

logger = get_logger(__name__)


def calculate_tam(
    params: TAMParameters, benchmark_tam_crores: Optional[float] = 1200.0
) -> TAMResult:
    """Computes bottom-up TAM from demographic and adoption parameters.

    Formula:
      Households = Population / Household_Size
      Connected HH = Households * Internet_Penetration
      Active eCommerce HH = Connected HH * eCommerce_Adoption
      Target Customers = Active eCommerce HH * Category_Share
      Annual Orders = Target Customers * Orders_Per_Month * 12
      Annual TAM = Annual Orders * Average_Order_Value

    Args:
        params: Structured demographic and consumption parameters.
        benchmark_tam_crores: Reference TAM in INR Crores for sanity checks.

    Returns:
        TAMResult dataclass with complete calculation breakdown.
    """
    logger.info("Executing bottom-up TAM estimation for %s...", params.target_city)

    households = int(params.population / params.household_size)
    connected_hh = int(households * params.internet_penetration_rate)
    ecommerce_hh = int(connected_hh * params.ecommerce_adoption_rate)
    target_customers = int(ecommerce_hh * params.target_category_share)

    annual_order_volume = int(target_customers * params.orders_per_month_per_hh * 12)
    annual_tam_inr = float(annual_order_volume * params.average_order_value)
    annual_tam_crores = annual_tam_inr / 1e7

    variance_pct = 0.0
    sanity_passed = True
    if benchmark_tam_crores and benchmark_tam_crores > 0:
        variance_pct = round(
            (annual_tam_crores - benchmark_tam_crores) / benchmark_tam_crores * 100,
            2,
        )
        if abs(variance_pct) > 150.0:
            sanity_passed = False
            logger.warning(
                "TAM sanity check warning: Calculated TAM (INR %.2f Cr) deviates"
                " by %.2f%% from benchmark (INR %.2f Cr).",
                annual_tam_crores,
                variance_pct,
                benchmark_tam_crores,
            )

    result = TAMResult(
        city=params.target_city,
        total_households=households,
        connected_households=connected_hh,
        active_ecommerce_households=ecommerce_hh,
        target_customers=target_customers,
        annual_order_volume=annual_order_volume,
        annual_tam_inr=round(annual_tam_inr, 2),
        annual_tam_inr_crores=round(annual_tam_crores, 2),
        sanity_check_passed=sanity_passed,
        benchmark_variance_pct=variance_pct,
    )

    logger.info(
        "TAM Sizing Complete for %s: Target Customers: %s, Annual TAM:"
        " INR %.2f Crores",
        params.target_city,
        f"{target_customers:,}",
        annual_tam_crores,
    )
    return result


def get_default_bengaluru_tam() -> TAMResult:
    """Returns baseline TAM calculation for Bengaluru market."""
    params = TAMParameters(
        target_city="Bengaluru",
        population=12500000,
        household_size=4.0,
        internet_penetration_rate=0.75,
        ecommerce_adoption_rate=0.22,
        target_category_share=0.35,
        orders_per_month_per_hh=2.0,
        average_order_value=450.0,
    )
    return calculate_tam(params, benchmark_tam_crores=1200.0)


if __name__ == "__main__":
    res = get_default_bengaluru_tam()
    print("TAM Result:\n", res)
