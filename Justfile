# Project orchestration with just

# Usage:
#   just up [dev|prod]      # Start all stacks (default: prod)
#   just build [dev|prod]   # Build all stacks (default: prod)
#   just down [dev|prod]    # Stop all stacks (default: prod)
#   just logs [dev|prod]    # Tail logs for all stacks (default: prod)
#   just status [dev|prod]  # Show status for all stacks (default: prod)

build PROFILE="prod":
    ./scripts/orchestrate.sh build {{PROFILE}}

up PROFILE="prod":
    ./scripts/orchestrate.sh up {{PROFILE}}

deploy: 
    ./scripts/orchestrate.sh build prod
    ./scripts/orchestrate.sh up prod

down PROFILE="prod":
    ./scripts/orchestrate.sh down {{PROFILE}}

logs PROFILE="prod":
    ./scripts/orchestrate.sh logs {{PROFILE}}

status PROFILE="prod":
    ./scripts/orchestrate.sh status {{PROFILE}} 