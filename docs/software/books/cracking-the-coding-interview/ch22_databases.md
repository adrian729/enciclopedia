# Ch 22: Databases

## Table of Contents

- [1. SQL syntax and variations](#1-sql-syntax-and-variations)
- [2. Normalized vs. denormalized databases](#2-normalized-vs-denormalized-databases)
- [3. Common SQL query pitfalls](#3-common-sql-query-pitfalls)
- [4. Small database design](#4-small-database-design)
- [5. Large database design](#5-large-database-design)

Candidates who claim database experience may be asked to demonstrate it through SQL queries or database design. Examples in the book are tested against **Microsoft SQL Server**; minor syntax variations across SQL flavors are expected.

## 1. SQL syntax and variations

- **Implicit join vs. explicit join** — both are common and equivalent; choice is personal preference. The book uses explicit joins for consistency.

```sql
/* Explicit Join */
SELECT CourseName, TeacherName
FROM   Courses INNER JOIN Teachers
ON     Courses.TeacherID = Teachers.TeacherID

/* Implicit Join */
SELECT CourseName, TeacherName
FROM   Courses, Teachers
WHERE  Courses.TeacherID = Teachers.TeacherID
```

## 2. Normalized vs. denormalized databases

| Aspect | Normalized | Denormalized |
|--------|------------|--------------|
| **Goal** | Minimize redundancy | Optimize read time |
| **Data duplication** | Stored once (e.g., teacher name lives only in `Teacher`, referenced via `TeacherID` foreign key) | Redundant copies (e.g., teacher name stored inside `Courses`) |
| **Tradeoff** | Expensive joins on common queries | Faster reads at the cost of duplicated data |
| **Typical use** | Traditional relational design | **Highly scalable systems** |

## 3. Common SQL query pitfalls

Using the schema `Courses`, `Teachers`, `Students`, `StudentCourses`, consider the query "list all students and how many courses each is enrolled in." A naive `INNER JOIN` + `count(*)` + `GROUP BY StudentID` has three problems:

1. **`INNER JOIN` excludes unenrolled students** — must use `LEFT JOIN` so students with zero courses appear.
2. **`count(*)` is wrong after a `LEFT JOIN`** — unenrolled students still produce one row in their group, giving count `1` instead of `0`. Use `count(StudentCourses.CourseID)` so NULLs are not counted.
3. **`StudentName` is ambiguous under `GROUP BY StudentID`** — SQL forbids selecting non-aggregate columns outside the `GROUP BY`. Resolve by (a) wrapping with an outer query that joins back to `Students`, (b) adding `StudentName` to the `GROUP BY`, or (c) wrapping it in an aggregate like `max(StudentName)`.

- **Handle NULLs from outer joins in `SELECT`** — e.g., `isnull(StudentSize.Number, 0)` converts NULL student counts to zero when listing teachers who may have no classes.

## 4. Small database design

Four-step approach, analogous to object-oriented design.

| Step | Action |
|------|--------|
| **1. Handle Ambiguity** | Clarify scope with the interviewer before designing (e.g., does an apartment rental agency have multiple locations? Can one person rent two apartments in the same building?). Rare cases may warrant a workaround rather than schema support. |
| **2. Define the Core Objects** | Identify core entities; each typically becomes a table (e.g., `Property`, `Building`, `Apartment`, `Tenant`, `Manager`). |
| **3. Analyze Relationships** | Determine one-to-many vs. many-to-many. One-to-many adds a foreign key on the "many" side (e.g., `Apartments.BuildingID`). Many-to-many requires a junction table (e.g., `TenantApartments(TenantID, ApartmentID)`). |
| **4. Investigate Actions** | Walk through typical actions (leases, move-outs, rent payments) to surface missing tables and columns. |

## 5. Large database design

- **Joins are very slow at scale** — large-system design should avoid them where possible.
- **Denormalize deliberately** — duplicate data across tables based on how it will be read.
- **Design around access patterns** — think carefully about how data will be used before choosing a schema.
