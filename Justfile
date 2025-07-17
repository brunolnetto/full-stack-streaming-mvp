# Project orchestration with just

# Usage:
#   just up [dev|prod]      # Start all stacks (default: prod)
#   just build [dev|prod]   # Build all stacks (default: prod)
#   just down [dev|prod]    # Stop all stacks (default: prod)
#   just logs [dev|prod]    # Tail logs for all stacks (default: prod)
#   just status [dev|prod]  # Show status for all stacks (default: prod)

build PROFILE="prod":
    ./orchestrate.sh build {{PROFILE}}

up PROFILE="prod":
    ./orchestrate.sh up {{PROFILE}}

deploy: 
    ./orchestrate.sh build prod
    ./orchestrate.sh up prod

down PROFILE="prod":
    ./orchestrate.sh down {{PROFILE}}

logs PROFILE="prod":
    ./orchestrate.sh logs {{PROFILE}}

status PROFILE="prod":
    ./orchestrate.sh status {{PROFILE}} 