# Save this as initial_migration.ps1 in your project root

# List of your app names
$apps = @("groupbuys", "orders", "products", "users", "wishlist")  # Adjust this list as needed

# Create migrations for each app
foreach ($app in $apps) {
    Write-Host "Creating migration for $app"
    python manage.py makemigrations $app
}

# Apply migrations
Write-Host "Applying migrations"
python manage.py migrate

Write-Host "Migration process completed!"