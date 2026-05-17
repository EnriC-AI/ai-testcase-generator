# AGENTS.md

## 📌 Project Overview
**Project Name:** `pytest-api-framework`

A modular and scalable API testing framework built with **PyTest** and designed to simulate a real-world QA Automation architecture.

The project demonstrates:
- API automation best practices
- Environment-driven execution
- Mock/static testing strategies
- CI/CD readiness
- Professional documentation and reporting

---

# 🎯 Main Goals
- Create a reusable API automation framework
- Improve maintainability and scalability
- Demonstrate senior-level QA engineering practices
- Prepare a portfolio/interview-ready project
- Support both mock and live API testing

---

# 🧱 Current Architecture

```text
pytest-api-framework/
│
├── config/
│   ├── dev.yaml
│   ├── mock.yaml
│   └── prod.yaml
│
├── core/
│   ├── api_client.py
│   ├── auth.py
│   └── config_loader.py
│
├── tests/
│   ├── test_smoke.py
│   ├── test_healthcheck.py
│   ├── test_create_user.py
│   └── test_users.py
│
├── reports/
├── logs/
├── utils/
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md