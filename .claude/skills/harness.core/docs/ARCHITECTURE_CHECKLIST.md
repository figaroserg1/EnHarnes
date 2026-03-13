# ARCHITECTURE.md Checklist

Use this checklist to validate an existing `ARCHITECTURE.md` or to write a proper new one.

## 1. Verify the file's purpose

- [ ] The file explains architecture, not setup, onboarding, or usage
- [ ] The file helps a new developer quickly understand the project structure
- [ ] The file describes the stable shape of the system, not small implementation details

## 2. Write a brief project overview

- [ ] Briefly explain what problem the project solves
- [ ] Briefly explain the main system flow
- [ ] List the key subsystems
- [ ] Remove history, fluff, and marketing language

## 3. Add a project codemap

- [ ] List the main directories, modules, or subsystems
- [ ] Briefly explain the purpose of each major part
- [ ] Show how the parts connect to each other
- [ ] Make it clear where to look for code related to a specific task
- [ ] Make it clear what each module does at a high level

## 4. Document architectural boundaries

- [ ] Clearly describe the main layers or boundaries in the system
- [ ] State what belongs to domain logic
- [ ] State what belongs to infrastructure
- [ ] State what is public API and what is internal implementation
- [ ] Describe module boundaries clearly enough to avoid ambiguous interpretation

## 5. Document architectural invariants

- [ ] State which dependencies are allowed
- [ ] State which dependencies are forbidden
- [ ] Describe rules that must not be broken when changing the code
- [ ] Explicitly document important non-obvious constraints

## 6. Describe cross-cutting concerns

- [ ] Explain where and how logging is handled
- [ ] Explain how configuration is handled
- [ ] Explain how error handling is handled
- [ ] Document common rules for security, observability, feature flags, or other cross-cutting concerns
- [ ] Keep these descriptions at the architectural level, without unnecessary low-level detail

## 7. Check the level of detail

- [ ] The file is short and easy to reread
- [ ] The file does not describe every function
- [ ] The file does not include excessive implementation detail
- [ ] The file avoids fast-changing specifics
- [ ] The file names important entities: directories, modules, files, services, interfaces, and key types

## 8. Check how code is referenced

- [ ] Refer to entities by name
- [ ] Do not use fragile links to specific lines of code
- [ ] Use names that are precise enough to be found quickly via repository search

## 9. Check what should not be included

- [ ] No install guide
- [ ] No run commands unless they are necessary to understand the architecture
- [ ] No README-style product description in place of architecture
- [ ] No pasted code
- [ ] No temporary implementation details presented as architectural truth
- [ ] No vague wording where concrete module or subsystem names should be used

## 10. Final quality check

- [ ] A new developer can quickly build a mental model of the project
- [ ] A new developer can understand where to go in the code
- [ ] A new developer can understand which boundaries and rules must not be violated
- [ ] The file genuinely helps navigation and decision-making, not just formal documentation
