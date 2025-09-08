from fastmcp import FastMCP
import httpx
import logging
from typing import Optional, Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("Productboard API Server")

# API configuration
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJraWQiOiJlYWQ0MWY3NmE1M2E5OGNmOGIxZjI2NTA5Mzg2ZThmNGM1OWYzMzg5ZTljMDQ0YjQ2NjRkYThjYzY5NjdkY2Q2IiwiYWxnIjoiUlM1MTIifQ.eyJpYXQiOjE3NTU2MTM3ODEsImlzcyI6IjY5N2FiYTc4LWM5MjAtNGNiNS1hNTNjLWZhM2QxN2QxMTA4MyIsInN1YiI6IjE1MjExMzUiLCJyb2xlIjoiYWRtaW4iLCJhdWQiOiJodHRwczovL2FwaS5wcm9kdWN0Ym9hcmQuY29tIiwidXNlcl9pZCI6MTUyMTEzNSwic3BhY2VfaWQiOiIzNDk0NDIifQ.mIu-C_SV2FOpeSPgrUa3yJHc2SU3MssXIdrZJbHb0mCnKfzhggiRqCkW1d2pp48Aaf6cPmKZ0i54Sxms5KHt52Ik7IincSiHTvQbHxMRXb5gYp-1hKI3BxhzYn-BrLAnZdf4GbYmKdlKsr13u5M5i4ak9w6cNbX4fUejVZ2L1NRfPjDzGE3yb1hlyub9dy0X7XN_6ShML4ImzJSRns33aaZZ6I7Fw5VXw2uRrSPcXGSlLExUpCrR1GM9EPn34aXqriyF4mMrKa71UqNY3NLcjYzPUTeFP708ByE26HMi3fY6lepr8sDzK8WnRVwSWfA4fd4A_AkVFrLJmvQ9OUXSBg"
BASE_URL = "https://api.productboard.com"

# Helper function to build headers
def build_headers(content_type: str = "application/json") -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": content_type,
        "X-Version": "1"
    }

@mcp.tool()
def create_note(title: str, content: str, display_url: Optional[str] = None, user: Optional[Dict[str, Any]] = None, company: Optional[Dict[str, Any]] = None, source: Optional[Dict[str, Any]] = None, owner: Optional[Dict[str, Any]] = None, tags: Optional[List[str]] = None) -> Dict[str, Any]:
    """Creates a new note in Productboard.
    Parameters:
        title (str): Title of the note.
        content (str): Content of the note (HTML allowed).
        display_url (Optional[str]): Optional display URL.
        user (Optional[dict]): Optional user info.
        company (Optional[dict]): Optional company info.
        source (Optional[dict]): Optional source info.
        owner (Optional[dict]): Optional owner info.
        tags (Optional[List[str]]): Optional list of tags.
    Returns:
        Dict with 'status' and data or error message.
    """
    logger.info(f"create_note called with title: {title}")
    url = f"{BASE_URL}/notes"
    headers = build_headers()
    payload = {
        "title": title,
        "content": content
    }
    if display_url is not None:
        payload["display_url"] = display_url
    if user is not None:
        payload["user"] = user
    if company is not None:
        payload["company"] = company
    if source is not None:
        payload["source"] = source
    if owner is not None:
        payload["owner"] = owner
    if tags is not None:
        payload["tags"] = tags

    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        logger.info("create_note executed successfully")
        return {"status": "success", "data": response.json()}
    except Exception as e:
        logger.error(f"Error in create_note: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def list_notes(last: Optional[str] = None, created_from: Optional[str] = None, created_to: Optional[str] = None, page_limit: Optional[int] = 50, page_cursor: Optional[str] = None) -> Dict[str, Any]:
    """Retrieves a paginated list of all notes.
    Parameters:
        last (Optional[str]): Filter for last note id.
        created_from (Optional[str]): Filter for creation start date.
        created_to (Optional[str]): Filter for creation end date.
        page_limit (Optional[int]): Number of items per page.
        page_cursor (Optional[str]): Cursor for pagination.
    Returns:
        Dict with 'status' and data or error message.
    """
    logger.info("list_notes called")
    url = f"{BASE_URL}/notes"
    headers = build_headers()
    params = {}
    if last is not None:
        params['last'] = last
    if created_from is not None:
        params['createdFrom'] = created_from
    if created_to is not None:
        params['createdTo'] = created_to
    if page_limit is not None:
        params['pageLimit'] = page_limit
    if page_cursor is not None:
        params['pageCursor'] = page_cursor

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=30.0)
        response.raise_for_status()
        logger.info("list_notes executed successfully")
        return {"status": "success", "data": response.json()}
    except Exception as e:
        logger.error(f"Error in list_notes: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def create_company(name: str, domain: Optional[str] = None) -> Dict[str, Any]:
    """Creates a new company.
    Parameters:
        name (str): Name of the company.
        domain (Optional[str]): Domain of the company.
    Returns:
        Dict with 'status' and data or error message.
    """
    logger.info(f"create_company called with name: {name}")
    url = f"{BASE_URL}/companies"
    headers = build_headers()
    payload = {"name": name}
    if domain is not None:
        payload["domain"] = domain

    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        logger.info("create_company executed successfully")
        return {"status": "success", "data": response.json()}
    except Exception as e:
        logger.error(f"Error in create_company: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def list_companies(limit: Optional[int] = 20, offset: Optional[int] = 0) -> Dict[str, Any]:
    """Retrieves a list of all companies.
    Parameters:
        limit (Optional[int]): Maximum number of companies.
        offset (Optional[int]): Offset for pagination.
    Returns:
        Dict with 'status' and data or error message.
    """
    logger.info("list_companies called")
    url = f"{BASE_URL}/companies"
    headers = build_headers()
    params = {"limit": limit, "offset": offset}

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=30.0)
        response.raise_for_status()
        logger.info("list_companies executed successfully")
        return {"status": "success", "data": response.json()}
    except Exception as e:
        logger.error(f"Error in list_companies: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def create_feature(name: str, description: Optional[str] = None, parent: Optional[Dict[str, str]] = None, type: Optional[str] = None) -> Dict[str, Any]:
    """Creates a new feature.
    Parameters:
        name (str): Name of the feature.
        description (Optional[str]): Description of the feature.
        parent (Optional[dict]): Parent feature info with id.
        type (Optional[str]): Type of the feature.
    Returns:
        Dict with 'status' and data or error message.
    """
    logger.info(f"create_feature called with name: {name}")
    url = f"{BASE_URL}/features"
    headers = build_headers()
    payload = {"name": name}
    if description is not None:
        payload["description"] = description
    if parent is not None:
        payload["parent"] = parent
    if type is not None:
        payload["type"] = type

    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        logger.info("create_feature executed successfully")
        return {"status": "success", "data": response.json()}
    except Exception as e:
        logger.error(f"Error in create_feature: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def list_features(limit: Optional[int] = 10, offset: Optional[int] = 0, status_name: Optional[str] = None) -> Dict[str, Any]:
    """Retrieves a list of all features.
    Parameters:
        limit (Optional[int]): Number of features to return.
        offset (Optional[int]): Offset for pagination.
        status_name (Optional[str]): Filter features by status name.
    Returns:
        Dict with 'status' and data or error message.
    """
    logger.info("list_features called")
    url = f"{BASE_URL}/features"
    headers = build_headers()
    params = {"limit": limit, "offset": offset}
    if status_name is not None:
        params['status.name'] = status_name

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=30.0)
        response.raise_for_status()
        logger.info("list_features executed successfully")
        return {"status": "success", "data": response.json()}
    except Exception as e:
        logger.error(f"Error in list_features: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def update_feature(feature_id: str, name: Optional[str] = None, description: Optional[str] = None, status: Optional[Dict[str, str]] = None, parent: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Updates an existing feature.
    Parameters:
        feature_id (str): ID of the feature to update.
        name (Optional[str]): New name of the feature.
        description (Optional[str]): New description.
        status (Optional[dict]): Dictionary with key 'id' for new status.
        parent (Optional[dict]): Dictionary with key 'id' for parent feature.
    Returns:
        Dict with 'status' and data or error message.
    """
    logger.info(f"update_feature called for ID: {feature_id}")
    url = f"{BASE_URL}/features/{feature_id}"
    headers = build_headers()
    payload = {}
    if name is not None:
        payload["name"] = name
    if description is not None:
        payload["description"] = description
    if status is not None:
        payload["status"] = status
    if parent is not None:
        payload["parent"] = parent

    try:
        response = httpx.patch(url, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        logger.info("update_feature executed successfully")
        return {"status": "success", "data": response.json()}
    except Exception as e:
        logger.error(f"Error in update_feature: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def list_custom_fields(field_type: str) -> Dict[str, Any]:
    """Returns definitions of all custom fields.
    Parameters:
        field_type (str): Type of custom fields (e.g., text, number).
    Returns:
        Dict with 'status' and data or error message.
    """
    logger.info(f"list_custom_fields called with type: {field_type}")
    url = f"{BASE_URL}/hierarchy-entities/custom-fields"
    headers = build_headers()
    params = {"type": field_type}

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=30.0)
        response.raise_for_status()
        logger.info("list_custom_fields executed successfully")
        return {"status": "success", "data": response.json()}
    except Exception as e:
        logger.error(f"Error in list_custom_fields: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def set_custom_field_value(custom_field_id: str, hierarchy_entity_id: str, value: Any) -> Dict[str, Any]:
    """Sets a custom field value on a hierarchy entity.
    Parameters:
        custom_field_id (str): ID of the custom field.
        hierarchy_entity_id (str): ID of the hierarchy entity.
        value (Any): The value to set (can be string, number, list, or object).
    Returns:
        Dict with 'status' and data or error message.
    """
    logger.info(f"set_custom_field_value called for custom_field_id: {custom_field_id} and hierarchy_entity_id: {hierarchy_entity_id}")
    url = f"{BASE_URL}/hierarchy-entities/custom-fields-values/value"
    headers = build_headers()
    params = {"customField.id": custom_field_id, "hierarchyEntity.id": hierarchy_entity_id}

    try:
        response = httpx.put(url, headers=headers, params=params, json=value, timeout=30.0)
        response.raise_for_status()
        logger.info("set_custom_field_value executed successfully")
        return {"status": "success", "data": response.json()}
    except Exception as e:
        logger.error(f"Error in set_custom_field_value: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def list_releases(release_group_id: Optional[str] = None, limit: Optional[int] = 10, offset: Optional[int] = 0) -> Dict[str, Any]:
    """Retrieves a list of all releases.
    Parameters:
        release_group_id (Optional[str]): Filter by release group ID.
        limit (Optional[int]): Maximum number of releases.
        offset (Optional[int]): Offset for pagination.
    Returns:
        Dict with 'status' and data or error message.
    """
    logger.info("list_releases called")
    url = f"{BASE_URL}/releases"
    headers = build_headers()
    params = {"limit": limit, "offset": offset}
    if release_group_id is not None:
        params['releaseGroup.id'] = release_group_id

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=30.0)
        response.raise_for_status()
        logger.info("list_releases executed successfully")
        return {"status": "success", "data": response.json()}
    except Exception as e:
        logger.error(f"Error in list_releases: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def create_subscription(events: List[str], notification_url: str, notification_version: int) -> Dict[str, Any]:
    """Creates a new webhook subscription.
    Parameters:
        events (List[str]): List of events to subscribe to.
        notification_url (str): URL that receives webhook notifications.
        notification_version (int): Version of the notification protocol.
    Returns:
        Dict with 'status' and data or error message.
    """
    logger.info("create_subscription called")
    url = f"{BASE_URL}/webhooks"
    headers = build_headers()
    payload = {
        "data": {
            "events": events,
            "notification": {
                "url": notification_url,
                "version": notification_version
            }
        }
    }

    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        logger.info("create_subscription executed successfully")
        return {"status": "success", "data": response.json()}
    except Exception as e:
        logger.error(f"Error in create_subscription: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def list_components(limit: Optional[int] = 10, offset: Optional[int] = 0) -> Dict[str, Any]:
    """Retrieves a list of all components.
    Parameters:
        limit (Optional[int]): Maximum number of components.
        offset (Optional[int]): Offset for pagination.
    Returns:
        Dict with 'status' and data or error message.
    """
    logger.info("list_components called")
    url = f"{BASE_URL}/components"
    headers = build_headers()
    params = {"limit": limit, "offset": offset}

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=30.0)
        response.raise_for_status()
        logger.info("list_components executed successfully")
        return {"status": "success", "data": response.json()}
    except Exception as e:
        logger.error(f"Error in list_components: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def health_check() -> Dict[str, Any]:
    """Health check endpoint.
    Returns server status and list of available tools.
    """
    logger.info("health_check called")
    tool_names = [
        'create_note', 'list_notes', 'create_company', 'list_companies', 'create_feature', 'list_features',
        'update_feature', 'list_custom_fields', 'set_custom_field_value', 'list_releases', 'create_subscription', 'list_components'
    ]
    return {
        "status": "healthy",
        "server": "Productboard MCP Server",
        "tools": tool_names
    }

if __name__ == "__main__":
    logger.info("Starting Productboard FastMCP server...")
    mcp.run(transport="http", port=8080, host="0.0.0.0")
