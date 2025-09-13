# Field Operator Tracker
## Purpose

The Field Operator Tracker is designed to help companies manage, monitor, and log the activities of field agents.
It tracks daily assignments, location check-ins, visit notes, and task statuses in real-time through a clean backend interface.

## Problem Statement

Organizations with field employees often lack a structured system to:

| Task | Description |
| --- | --- |
| Assign daily tasks |  |
| Record visit locations and times |  |
| Track progress and completion status |  |
| Log summaries for customer visits or operational checks |  |

## Use Cases

1. Manager assigns daily visits to field operators.
2. Field operators check-in with location and timestamp.
3. Field operators write quick visit notes.
4. Manager tracks task status live (Pending → In Progress → Completed).
5. HR or Management generates reports on agent performance.

## Target User Personas

| User Role | Description | Permissions |
| --- | --- | --- |
| Field Operator | Employee completing field tasks. | Can see and edit their assigned tasks only. |
| Field Manager | Supervisor assigning tasks. | Can create, assign, and view all tasks. |
| Administrator | Full control over module. | Can manage settings, fields, and records. |

## Features

| Feature | UI Elements to Create | Backend Models |
| --- | --- | --- |
| Task Management | Menu Item: "Field Tasks", Action Window, Kanban/List View, Form View | field.operator.task |
| Assignment to Users | Many2one field on task model | - |
| Location Check-ins | Field for manual or auto-fill GPS location (Phase 2 idea) | - |
| Status Tracking | Status Bar (Selection Field) | - |
| Visit Notes | Notes Field on Form View | - |
| Chatter Log | Enable chatter on task records | - |

## Technical Structure

### Backend Model

* Main model: field.operator.task
* Folder: models/field_operator.py

### Views

| View Type | File Name | Content |
| --- | --- | --- |
| List View | views/field_operator_task_views.xml | Columns: Title, Assigned To, Location, Status |
| Form View | views/field_operator_task_views.xml | Full record view, Chatter enabled |
| Kanban View (Optional Phase 2) | views/field_operator_task_kanban.xml | Task cards with statuses |
| Menu | views/field_operator_menus.xml | Main menu under 'Field Service' or 'Operations' |
| Security | security/ir.model.access.csv | User permissions |

## Naming Conventions

| Element | Rule | Example |
| --- | --- | --- |
| Models (_name) | lowercase, dot separated | field.operator.task |
| Views Files | module name + feature description | field_operator_task_views.xml |
| Menus | module name + menus | field_operator_menus.xml |
| Security | standard ir.model.access.csv + optional security.xml for advanced | ir.model.access.csv |
| Data Files | Placed in /data/ folder if static data like stages or statuses | - |
| Fields | snake_case | assigned_to, check_in_time |
| DateTime Fields | Use fields.Datetime in models | check_in_time = fields.Datetime(...) |
| Relations | Many2one, One2many standard use | assigned_to = fields.Many2one('res.users', ...) |

## Attribute Specifics

| Attribute | Recommendation | Reason |
| --- | --- | --- |
| Datetime | Use fields.Datetime with UTC assumed | Standard in Odoo, better for scheduling |
| Tracking | Set tracking=True on important fields | Enables chatter logs |
| Status Fields | Always use fields.Selection | For controlled statuses like 'pending', 'in_progress', etc. |
| Access Rights | Use ir.model.access.csv first | Easier management via groups |

## Folder Layout

field_ops_tracker/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── field_operator.py
├── views/
│   ├── field_operator_task_views.xml
│   ├── field_operator_menus.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml (optional advanced rules)
├── static/
│   ├── description/
│   │   └── icon.png
├── data/
│   └── predefined_statuses.xml (optional if you pre-load data)

## Example Access Rights (CSV)

id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_field_operator_task_user,field.operator.task.user,model_field_operator_task,base.group_user,1,1,1,0
access_field_operator_task_manager,field.operator.task.manager,model_field_operator_task,base.group_system,1,1,1,1

    Users can create and edit their own tasks but not delete.

    Managers/Admins can create, edit, and delete.

## Deployment Plan (optional)

| Phase | Goal |
| --- | --- |
| Phase 1 | Backend module ready: Create, assign, track tasks |
| Phase 2 | Add GPS autofill for location check-in |
| Phase 3 | Mobile responsiveness + Kanban board view for fid agents |

## Closing Notes

    Stick to clean snake_case fields.

    Always define access rights properly early on.

    Use chatter (mail.thread) to let managers and users track history effortlessly.

    When using Datetime fields, assume UTC timezone unless localization is added.

    Keep all views modular — separate menus, views, templates for future scaling.

