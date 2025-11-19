# Intelligent Monorepo Build Tooling

A scalable build infrastructure designed to enhance Developer Experience (DevEx) by automating flakiness detection and standardizing module configurations.

## Project Goal
To reduce "Build Toil" and feedback loops for engineering teams working in large-scale Kotlin/Java Monorepos. This project implements a self-healing build agent that detects non-deterministic tests (flakiness) before they block CI pipelines.

## Tech Stack
* **Build System:** Gradle (Kotlin DSL) with Composite Builds (`build-logic`)
* **Language:** Kotlin (Application), Python (Automation)
* **Infrastructure:** Docker (Reproducible Build Agents)
* **Testing:** JUnit 5 with Parallel Execution Strategy

## Key Features

### 1. Self-Healing Build Agent (`tools/deflaker.py`)
Automated wrapper that intercepts build exit codes.
* **Problem:** Flaky tests (network timeouts, race conditions) cause 30% of CI failures, requiring manual restarts.
* **Solution:** A Python-based heuristic that retries failures locally. If a test passes on retry, it is tagged as **"Flaky"** (severity: warning) rather than **"Failed"** (severity: blocker).

### 2. Standardization Plugins (`build-logic`)
Custom Gradle Convention Plugins to enforce consistency across microservices.
* Centralized Java Toolchains (Java 21).
* Unified Test Logging & Parallel Execution policies.
* Decoupled dependency management using Version Catalogs (`libs.versions.toml`).

### 3. Containerized Infrastructure
* Fully dockerized build environment ensuring parity between local development and CI agents.
* Eliminates "works on my machine" issues regarding JDK versions or Gradle distributions.

## How to Run

**1. Build the Agent**
```bash
docker build -t build-tooling-agent .
````

**2. Run the Self-Healing Pipeline**

```bash
docker run --rm build-tooling-agent
```

## Simulated Scenarios

The repository contains a `core-banking` module with a programmed probabilistic failure (`FlakyTest.kt`) to demonstrate the automation's ability to recover from infrastructure instability (e.g., 503 Service Unavailable simulations).
