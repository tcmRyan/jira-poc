-- name: insert_authentication(key, client_key, shared_secret, plugins_version, base_url, product_type, description, service_entitlement_number, event_type, public_key, server_version, installed_by)!
-- Store the tenant details Atlassian sends when the add-on is installed.
INSERT INTO authentications (
    "key", "clientKey", "sharedSecret", "pluginsVersion", "baseUrl", "productType",
    "description", "serviceEntitlementNumber", "eventType", "publicKey",
    "serverVersion", "installedBy"
) VALUES (
    :key, :client_key, :shared_secret, :plugins_version, :base_url, :product_type,
    :description, :service_entitlement_number, :event_type, :public_key,
    :server_version, :installed_by
);

-- name: get_authentication_by_base_url(base_url)^
-- Fetch the first tenant installed on the given Atlassian base url.
SELECT *
  FROM authentications
 WHERE "baseUrl" = :base_url
 ORDER BY id
 LIMIT 1;

-- name: delete_authentications_by_client_key(client_key)!
-- Remove every tenant record for the given client key when the add-on is uninstalled.
DELETE FROM authentications
 WHERE "clientKey" = :client_key;
