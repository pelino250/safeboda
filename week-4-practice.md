# SafeBoda API Documentation and Performance Testing Activity

**Group Size:** 4 students per group

## Learning Objectives

By the end of this activity, you will:
- Document REST APIs using industry-standard tools
- Test API endpoints systematically using Postman
- Implement and verify caching strategies
- Use Django Debug Toolbar to analyze performance
- Understand the impact of caching on API performance

---

## Pre-Activity Setup

### Repository Setup
1. Pull the latest changes from your SafeBoda repository
2. Ensure your authentication implementation is working
3. Activate your virtual environment
4. Verify the development server runs without errors

### Install Required Tools
- Postman Desktop App: https://www.postman.com/downloads/
- Or use Thunder Client (VS Code extension) as an alternative

---

## Part 1: Installing Django Debug Toolbar

**Documentation Reference:**
- Official Django Debug Toolbar Docs: https://django-debug-toolbar.readthedocs.io/en/latest/installation.html

### Installation Steps

1. **Install the Package**
   - Add django-debug-toolbar to your requirements.txt
   - Install via pip

2. **Configure Settings**
   - Add 'debug_toolbar' to INSTALLED_APPS
   - Add debug toolbar middleware (position matters - check docs)
   - Configure INTERNAL_IPS to include '127.0.0.1'
   - Ensure DEBUG = True in your development settings

3. **Update URLs**
   - Import debug_toolbar in your main urls.py
   - Add debug toolbar URLs (only when DEBUG is True)
   - Use conditional import to avoid issues in production

4. **Verify Installation**
   - Run the development server
   - Visit any page
   - Confirm the Debug Toolbar appears on the right side
   - Click through the different panels (SQL, Cache, Time, etc.)

**Key Panels to Explore:**
- SQL: Database query analysis
- Cache: Cache hit/miss statistics
- Time: Request/response timing
- HTTP: Request headers and metadata

---

## Part 2: Implementing Caching

**Documentation References:**
- Django Cache Framework: https://docs.djangoproject.com/en/stable/topics/cache/
- DRF Caching: https://www.django-rest-framework.org/api-guide/caching/

### Task: Implement Two Types of Caching

#### A. Per-View Caching

1. **Configure Cache Backend**
   - Add CACHES configuration in settings.py
   - Use LocMemCache for development (simple, in-memory)
   - Alternative: Redis or Memcached for production-like testing

2. **Apply cache_page Decorator**
   - Import cache_page from django.views.decorators.cache
   - Apply to a view that returns list data (e.g., riders list)
   - Set cache timeout (e.g., 60 seconds for testing)

3. **Test Cache Behavior**
   - Make request and note response time
   - Make same request again - should be faster
   - Check Debug Toolbar Cache panel for hits/misses

#### B. Low-Level Caching (Advanced)

1. **Import Cache Functions**
   - Use django.core.cache

2. **Implement Custom Cache Logic**
   - Cache expensive query results
   - Set appropriate cache keys
   - Handle cache invalidation
   - Example: Cache user profile data or aggregated statistics

3. **Verify with Debug Toolbar**
   - Check cache operations in Cache panel
   - Monitor cache hit ratio
   - Observe query count reduction in SQL panel

---

## Part 3: API Documentation

### Choose Your Documentation Approach

#### Option A: Django REST Framework's Built-in Documentation

**Reference:** https://www.django-rest-framework.org/topics/documenting-your-api/

1. **Install Core Schema Generation**
   - Install coreapi or uritemplate if needed
   - Check DRF documentation for current recommended approach

2. **Add Schema View**
   - Import schema generation views
   - Add schema endpoint to urls
   - Configure schema generator

3. **Generate API Documentation**
   - Add get_schema_view or similar
   - Include title, description, version
   - Configure authentication classes

4. **Test Documentation**
   - Visit the schema endpoint
   - Verify all endpoints are listed
   - Check parameter descriptions

#### Option B: drf-spectacular (OpenAPI/Swagger)

**Reference:** https://drf-spectacular.readthedocs.io/en/latest/

1. **Install drf-spectacular**
   - Add to requirements.txt and install
   - Add to INSTALLED_APPS

2. **Configure Settings**
   - Set up SPECTACULAR_SETTINGS dictionary
   - Configure title, version, description
   - Set up authentication schemes

3. **Add URLs**
   - Include schema view
   - Include Swagger UI view
   - Include ReDoc view (alternative documentation UI)

4. **Enhance Documentation**
   - Add docstrings to your views
   - Use extend_schema decorator for detailed endpoint documentation
   - Document request/response schemas

---

## Part 4: Postman Testing

**Postman Learning Center:** https://learning.postman.com/docs/getting-started/introduction/

### Create a Postman Collection

1. **Setup Collection**
   - Create new collection: "SafeBoda API"
   - Add collection description
   - Configure collection-level variables (base_url, auth_token)

2. **Create Request Folders**
   - Authentication
   - Users
   - Riders
   - (Add others based on your implementation)

3. **Document Each Endpoint**

   For each API endpoint, create a request with:
   - Appropriate HTTP method (GET, POST, PUT, DELETE)
   - Correct URL with path parameters
   - Required headers (Content-Type, Authorization)
   - Request body (for POST/PUT) with example data
   - Pre-request scripts (if needed for auth)
   - Tests tab with assertions

4. **Add Environment Variables**
   - Create "Development" environment
   - Add variables: base_url, email, password, token
   - Use variables in requests: {{base_url}}/api/profile/

### Write Postman Tests

Add tests to verify responses:
- Status code validation
- Response time checks
- Data structure validation
- Specific field verification

Example test structure:
```javascript
// Check status code
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Check response time
pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

// Validate JSON structure
pm.test("Response has required fields", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('email');
    pm.expect(jsonData).to.have.property('user_type');
});
```

---

## Part 5: Cache Performance Testing

### Testing Methodology

1. **Identify Test Endpoint**
   - Choose an endpoint with caching implemented
   - Preferably one that queries database

2. **First Request (Cache Miss)**
   - Clear Django cache (use management command or restart server)
   - Make request via Postman
   - Note response time in Postman
   - Check Debug Toolbar:
     - Number of SQL queries
     - Cache misses
     - Total request time

3. **Second Request (Cache Hit)**
   - Make identical request
   - Note response time (should be faster)
   - Check Debug Toolbar:
     - Number of SQL queries (should be fewer or zero)
     - Cache hits
     - Reduced request time

4. **Document Findings**
   - Create a comparison table
   - Calculate performance improvement percentage
   - Identify which queries were eliminated

### Cache Invalidation Testing

1. **Modify Data**
   - Update data that should invalidate cache
   - Make API request
   - Verify fresh data is returned

2. **Verify Cache Refresh**
   - Check if cache was properly invalidated
   - Confirm new data is now cached

---

## Deliverables

### 1. Updated Repository

**Branch name:** `api-docs-and-testing`

**Must include:**
- django-debug-toolbar configuration
- Cache implementation
- API documentation setup
- Updated requirements.txt

### 2. Postman Collection

**Export and include:**
- Complete Postman collection JSON file
- Save in repository: `/postman/SafeBoda_API.postman_collection.json`
- Environment variables file (sanitize sensitive data)

### 3. Documentation File

**Create:** `TESTING_GUIDE.md`

**Should contain:**

#### Debug Toolbar Setup
- Installation steps
- Configuration details
- How to access and use

#### Caching Implementation
- Cache strategy chosen
- Endpoints with caching
- Cache configuration details
- Invalidation strategy

#### API Documentation
- How to access API docs
- Documentation approach used
- Endpoint descriptions

#### Performance Analysis
- Cache performance comparison table
- Screenshots from Debug Toolbar showing:
  - SQL queries before/after caching
  - Cache hit/miss ratios
  - Response time improvements
- Analysis of results

#### Postman Testing Guide
- How to import collection
- How to set up environment
- How to run tests
- Expected test results

---

## Bonus Challenges

If you finish early:

1. **Advanced Caching**
   - Implement Redis instead of LocMemCache
   - Set up cache key versioning
   - Implement selective cache invalidation

2. **Enhanced Documentation**
   - Add request/response examples to docs
   - Include error response documentation
   - Add authentication flow diagrams

3. **Postman Automation**
   - Create collection runner sequence
   - Implement data-driven testing
   - Set up Newman for CLI testing

4. **Performance Benchmarking**
   - Use load testing tools (e.g., Locust, JMeter)
   - Compare different cache strategies
   - Generate performance reports

5. **Monitoring Setup**
   - Configure Django Debug Toolbar for specific metrics
   - Set up query profiling
   - Create performance dashboard

---

## Common Issues and Troubleshooting

### Debug Toolbar Not Appearing
- Check DEBUG = True
- Verify INTERNAL_IPS includes '127.0.0.1'
- Ensure middleware is properly ordered
- Check browser is not blocking the toolbar

### Cache Not Working
- Verify CACHES configuration is correct
- Check cache backend is properly installed
- Ensure cache keys are unique and valid
- Confirm cache timeout settings

### Postman Authentication Issues
- Check token/credentials format
- Verify Authorization header syntax
- Ensure environment variables are set
- Test authentication endpoint first

### API Documentation Not Generating
- Check all views are properly imported
- Verify schema generation is configured
- Ensure URL patterns are correct
- Check for circular import issues

---

## Submission Checklist

Before submitting, ensure:

- [ ] Debug toolbar is installed and functional
- [ ] At least two endpoints have caching implemented
- [ ] API documentation is accessible and complete
- [ ] Postman collection includes all endpoints
- [ ] All Postman tests pass
- [ ] TESTING_GUIDE.md is complete with screenshots
- [ ] Performance comparison data is documented
- [ ] Code is pushed to designated branch
- [ ] Postman collection is exported and committed
- [ ] All group members understand the implementation

---

## Resources

**Django Documentation:**
- Debug Toolbar: https://django-debug-toolbar.readthedocs.io/
- Caching: https://docs.djangoproject.com/en/stable/topics/cache/

**Django REST Framework:**
- Caching: https://www.django-rest-framework.org/api-guide/caching/
- Documentation: https://www.django-rest-framework.org/topics/documenting-your-api/

**Postman:**
- Learning Center: https://learning.postman.com/
- Writing Tests: https://learning.postman.com/docs/writing-scripts/test-scripts/

**Additional Tools:**
- drf-spectacular: https://drf-spectacular.readthedocs.io/
- Redis (optional): https://redis.io/docs/getting-started/

---

## Reflection Questions

After completing the activity:

1. How much did caching improve your API performance?
2. What are the trade-offs between different caching strategies?
3. When should you invalidate cache vs. letting it expire?
4. How does caching affect data consistency?
5. What metrics are most important when monitoring API performance?
6. How would you scale caching in a production environment?
7. What role does API documentation play in development workflow?
8. How can automated testing (Postman) improve development process?
