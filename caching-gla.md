# Comprehensive Caching Implementation Guide for Django SafeBoda

## **Learning Objectives**
By the end of this activity, students will be able to:
- Understand different types of caching in Django
- Implement Redis-based caching for API endpoints
- Create cache invalidation strategies
- Monitor cache performance
- Apply caching best practices

---

## **Activity 1: Understanding Caching Concepts**

### **Theory Check**
Before diving into implementation, answer these questions:

1. **What is caching and why is it important?**
   - Write a 2-sentence explanation
   - List 3 benefits of caching

2. **What are the different types of caching?**
   - Database query caching
   - Template caching
   - View caching
   - Full-page caching

3. **Cache Invalidation Challenge**
   - What problems can arise with stale cached data?
   - When should cache be cleared?

**Expected Time:** 15 minutes

---

## **Activity 2: Environment Setup (20 minutes)**

### **Step 1: Install Redis**

**For macOS:**
```shell script
brew install redis
brew services start redis
```


**For Ubuntu/Debian:**
```shell script
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```


**For Windows:**
```shell script
# Use Windows Subsystem for Linux or Docker
docker run -d -p 6379:6379 redis:alpine
```


### **Step 2: Verify Redis Installation**
```shell script
redis-cli ping
# Should return: PONG
```


### **Step 3: Update Requirements**
Add to your `requirements.txt`:
```
redis==5.0.1
django-redis==5.4.0
```


Install the new packages:
```shell script
pip install redis django-redis
```


### **Checkpoint Questions:**
- Can you connect to Redis?
- Are the new packages installed?
- What port is Redis running on?

---

## **Activity 3: Basic Cache Configuration**

### **Task 1: Configure Django Cache Settings**

**Your Mission:** Add Redis cache configuration to `settings.py`

**Hints:**
- Look for the DATABASES section
- Add a new CACHES dictionary
- Use 'django_redis.cache.RedisCache' as backend

**Template to complete:**
```python
CACHES = {
    'default': {
        'BACKEND': '_______________',  # Fill this
        'LOCATION': '_______________',  # Fill this (Redis URL)
        'TIMEOUT': ____,  # Default timeout in seconds
        'OPTIONS': {
            'CLIENT_CLASS': '_______________',  # Fill this
        }
    }
}

# Add cache timeout setting
CACHE_TTL = ___  # How many seconds?
```


**Test Your Configuration:**
Create a simple test in Django shell:
```python
python manage.py shell

from django.core.cache import cache
cache.set('test_key', 'Hello Cache!', 30)
print(cache.get('test_key'))
# Should print: Hello Cache!
```


### **Challenge Questions:**
1. What happens if Redis is not running?
2. How would you use different Redis databases for different cache types?
3. What's a reasonable default timeout for user data?

---

## **Activity 4: Implementing View-Level Caching (30 minutes)**

### **Task 1: Analyze Current UserViewSet**

**Study the existing code** and identify:
1. Which methods retrieve data from database?
2. Which methods modify data?
3. What would be good cache keys?

### **Task 2: Add Caching to UserViewSet**

**Your Mission:** Implement caching for the `list()` method

**Step-by-step Guide:**

1. **Import required modules** (add to views.py):
```python
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
```


2. **Create cache key helper function:**
```python
def get_cache_key(prefix, identifier=None):
    """Generate consistent cache keys"""
    if identifier:
        return f"{prefix}_{identifier}"
    return prefix
```


3. **Implement cached list method:**

Fill in the blanks:
```python
def list(self, request, *args, **kwargs):
    # Step 1: Create cache key
    cache_key = get_cache_key('_____')  # What should go here?
    
    # Step 2: Try to get from cache
    cached_data = cache._____(_______)  # Which method? What parameter?
    
    if cached_data is not None:
        return Response(cached_data)
    
    # Step 3: Get fresh data
    response = super().list(request, *args, **kwargs)
    
    # Step 4: Store in cache
    cache._____(_____,_____, timeout=_____)  # Fill the blanks
    
    return response
```


### **Task 3: Test Your Implementation**

1. **Create test data:**
```shell script
python manage.py shell

from users.models import User
User.objects.create_user(email='test@example.com', password='testpass', user_type='passenger')
```


2. **Test the API:**
```shell script
curl http://localhost:8000/api/users/
# Run this twice - second call should be faster
```


3. **Verify cache in Redis:**
```shell script
redis-cli
keys *
get user_list  # or whatever key you used
```


### **Challenge:**
- Add caching to the `retrieve()` method
- What cache key would you use for individual users?

---

## **Activity 5: Cache Invalidation Strategy (25 minutes)**

### **Task 1: Identify the Problem**

**Scenario:** You cached user list, but then created a new user via admin. What happens?

Test this:
1. Make API call to get user list (cache it)
2. Create new user in Django admin
3. Make API call again - do you see the new user?

### **Task 2: Implement Cache Invalidation**

**Your Mission:** Clear cache when data changes

**Template for create/update/delete methods:**
```python
def perform_create(self, serializer):
    # Clear relevant caches
    cache.delete('_____')  # What key?
    super().perform_create(serializer)

def perform_update(self, serializer):
    # Clear both list and individual caches
    user_id = serializer.instance.id
    cache.delete('_____')  # List cache
    cache.delete(f'user_{user_id}')  # Individual cache
    super().perform_update(serializer)
```


### **Task 3: Test Cache Invalidation**

1. Get user list (should cache)
2. Create new user via API
3. Get user list again (should show new user)

### **Advanced Challenge: Signal-Based Invalidation**

Create `users/cache_signals.py`:
```python
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def invalidate_user_cache(sender, instance, **kwargs):
    # What caches should be cleared?
    pass

@receiver(post_delete, sender=User)  
def invalidate_user_cache_on_delete(sender, instance, **kwargs):
    # What caches should be cleared?
    pass
```


**Connect the signals in apps.py:**
```python
def ready(self):
    import users.cache_signals
```


---

## **Activity 6: Cache Performance Monitoring (20 minutes)**

### **Task 1: Add Cache Metrics**

**Your Mission:** Track cache hit/miss ratios

**Create a simple decorator:**
```python
import functools
import time
import logging

logger = logging.getLogger(__name__)

def cache_performance(cache_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            logger.info(f"{cache_name}: {end_time - start_time:.4f}s")
            return result
        return wrapper
    return decorator
```


**Apply to your cached methods:**
```python
@cache_performance("user_list_cache")
def list(self, request, *args, **kwargs):
    # Your existing cached implementation
    pass
```


### **Task 2: Create Cache Statistics View**

**Challenge:** Create an endpoint that shows cache statistics

```python
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def cache_stats(request):
    # How would you check what's in cache?
    # What statistics would be useful?
    return Response({
        'cache_keys': [],  # List current cache keys
        'total_keys': 0,   # Count of cached items
        # Add more stats
    })
```


### **Task 3: Load Testing**

**Create a simple load test script:**
```python
# test_cache_performance.py
import requests
import time

def test_cache_performance():
    url = "http://localhost:8000/api/users/"
    
    # First call (cache miss)
    start = time.time()
    response1 = requests.get(url)
    time1 = time.time() - start
    
    # Second call (cache hit)
    start = time.time()
    response2 = requests.get(url)
    time2 = time.time() - start
    
    print(f"First call: {time1:.4f}s")
    print(f"Second call: {time2:.4f}s")
    print(f"Speedup: {time1/time2:.2f}x")

if __name__ == "__main__":
    test_cache_performance()
```


---

## **Activity 7: Advanced Caching Patterns (25 minutes)**

### **Task 1: Cache-Aside vs Write-Through**

**Implement cache-aside pattern** (what you've been doing):
- Check cache first
- If miss, get from DB and cache
- Manual cache invalidation

**Implement write-through pattern:**
```python
def perform_update(self, serializer):
    super().perform_update(serializer)
    
    # Write-through: immediately update cache
    user_data = self.get_serializer(serializer.instance).data
    cache_key = f"user_{serializer.instance.id}"
    cache.set(cache_key, user_data, timeout=settings.CACHE_TTL)
```


### **Task 2: Cache Warm-up**

**Create management command** for cache warming:

Create `users/management/commands/warm_cache.py`:
```python
from django.core.management.base import BaseCommand
from django.core.cache import cache
from users.models import User
from users.serializers import UserSerializer

class Command(BaseCommand):
    help = 'Warm up the cache with frequently accessed data'

    def handle(self, *args, **options):
        # Pre-cache user list
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        cache.set('user_list', serializer.data, timeout=3600)
        
        # Pre-cache individual users
        for user in users:
            user_data = UserSerializer(user).data
            cache.set(f'user_{user.id}', user_data, timeout=3600)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully cached {len(users)} users')
        )
```


### **Task 3: Cache Hierarchies**

**Implement cache tagging** for better invalidation:

```python
# Pseudo-code for cache tags
def cache_with_tags(key, data, tags, timeout=300):
    cache.set(key, data, timeout)
    for tag in tags:
        tagged_keys = cache.get(f'tag_{tag}', set())
        tagged_keys.add(key)
        cache.set(f'tag_{tag}', tagged_keys, timeout)

def invalidate_by_tag(tag):
    tagged_keys = cache.get(f'tag_{tag}', set())
    for key in tagged_keys:
        cache.delete(key)
    cache.delete(f'tag_{tag}')
```


---

## **Activity 8: Production Considerations (15 minutes)**

### **Discussion Points:**

1. **Cache Size Limits**
   - What happens when cache fills up?
   - LRU eviction policies
   - Memory monitoring

2. **Cache Distribution**
   - Single Redis vs Redis Cluster
   - Cache consistency across multiple servers
   - Failover strategies

3. **Security Considerations**
   - Sensitive data in cache
   - Cache key naming
   - Access controls

### **Task: Production Configuration**

**Create production cache settings:**
```python
# settings/production.py
if os.environ.get('REDIS_CLUSTER_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.environ.get('REDIS_CLUSTER_URL'),
            'OPTIONS': {
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 20,
                    'retry_on_timeout': True,
                },
            }
        }
    }
```


---

## **Activity 9: Challenge**

### **Practical Challenge:**

**Implement complete caching for Passenger model:**

1. Add Passenger list/detail caching
2. Implement proper invalidation
3. Add performance monitoring
4. Create cache warming command

### **Code Review Checklist:**

- [ ] Cache configuration is environment-specific
- [ ] Cache keys are consistent and descriptive
- [ ] Cache invalidation handles all CRUD operations
- [ ] Error handling for cache failures
- [ ] Performance monitoring is in place
- [ ] Cache timeouts are appropriate

### **Reflection Questions:**

1. What was the biggest challenge in implementing caching?
2. How would you explain cache invalidation to a junior developer?
3. What metrics would you monitor in production?
4. How would you handle cache failures gracefully?

---

## **Extension Activities:**

### **Advanced Challenges:**

1. **Implement cache versioning** to handle schema changes
2. **Add cache compression** for large datasets  
3. **Create cache analytics dashboard**
4. **Implement distributed cache locks** for concurrent updates
5. **Add cache preloading** based on user behavior patterns

### **Real-world Scenarios:**

1. **High Traffic Event:** How would you handle 10x traffic increase?
2. **Data Consistency:** Cache got out of sync with database - how to detect and fix?
3. **Memory Pressure:** Redis is running out of memory - what's your strategy?

---

## **Resources for Further Learning:**

- [Django Cache Framework Documentation](https://docs.djangoproject.com/en/5.2/topics/cache/)
- [Redis Best Practices](https://redis.io/docs/manual/clients-guide/)
- [Caching Strategies and Patterns](https://caching-patterns.com/)
