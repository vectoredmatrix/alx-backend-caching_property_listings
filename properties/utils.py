import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

# Initialize logger
logger = logging.getLogger(__name__)


def get_all_properties():
    """Get all properties, using Redis cache for 1 hour."""
    properties = cache.get('all_properties')
    if properties is None:
        logger.info("Cache miss — fetching from DB")
        properties = list(Property.objects.all().values())
        cache.set('all_properties', properties, 3600)
    else:
        logger.info("Cache hit — fetched from Redis")
    return properties


def get_redis_cache_metrics():
    """Retrieve and analyze Redis cache hit/miss metrics."""
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        # ✅ Calculate hit ratio safely
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio,
        }

        # ✅ Log metrics
        logger.info(f"Redis Cache Metrics → {metrics}")

        return metrics

    except Exception as e:
        # ✅ Log errors if Redis isn’t reachable or fails
        logger.error(f"Error fetching Redis metrics: {e}")
        return {"error": str(e)}
