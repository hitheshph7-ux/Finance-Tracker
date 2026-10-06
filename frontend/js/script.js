let API_URL = "http://127.0.0.1:8000/api";

async function resolveApiUrl() {
    let candidateUrls = [];
    if (window.location.origin && !window.location.origin.startsWith("file") && window.location.origin !== "null") {
        candidateUrls.push(`${window.location.origin}/api`);
    }
    candidateUrls.push("http://127.0.0.1:8000/api");
    candidateUrls.push("http://127.0.0.1:8001/api");
    candidateUrls.push("http://localhost:8000/api");
    candidateUrls.push("http://localhost:8001/api");

    for (const url of candidateUrls) {
        try {
            const controller = new AbortController();
            const tid = setTimeout(() => controller.abort(), 300);
            const res = await fetch(`${url}/income/`, { method: "GET", signal: controller.signal });
            clearTimeout(tid);
            if (res.ok || res.status < 500) {
                API_URL = url;
                return;
            }
        } catch (e) {}
    }
}

// Active user context
let currentUser = { id: 1, username: "" };
let allTransactions = [];
let categoriesList = [];
let currentTypeFilter = "all";
let currentCategoryFilter = "all";

// --- INITIALIZATION ---
document.addEventListener("DOMContentLoaded", async () => {
    await resolveApiUrl();
    const isAuthenticated = await checkAuthAndInitUser();
    if (!isAuthenticated) return;
    setTodayDates();
    loadCategories();
    loadAllData();
});

async function checkAuthAndInitUser() {
    const username = localStorage.getItem("username");
    if (!username) {
        window.location.href = "login.html";
        return false;
    }

    currentUser.username = username;

    const currentUserNameEl = document.getElementById("currentUserName");
    const displayUsernameEl = document.getElementById("displayUsername");
    if (currentUserNameEl) currentUserNameEl.textContent = username;
    if (displayUsernameEl) displayUsernameEl.textContent = username;

    try {
        const response = await fetch(`${API_URL}/user/${username}/`);
        if (response.ok) {
            const data = await response.json();
            if (data.user && data.user.id) {
                currentUser.id = data.user.id;
            }
        }
    } catch (err) {
        console.error("Failed to load user info:", err);
    }
    return true;
}

function logoutUser() {
    localStorage.removeItem("username");
    localStorage.removeItem("name");
    localStorage.removeItem("email");
    localStorage.removeItem("phone");
    localStorage.removeItem("occupation");
    localStorage.removeItem("income");
    window.location.href = "login.html";
}

// Toast Notifications
function showToast(message, type = "success") {
    const container = document.getElementById("toastContainer");
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    
    let icon = "✅";
    if (type === "error") icon = "❌";
    if (type === "info") icon = "ℹ️";
    
    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3500);
}

// Format Dates
function setTodayDates() {
    const today = new Date().toISOString().split("T")[0];
    const todayDisplay = new Date().toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
    
    const incomeDateEl = document.getElementById("incomeDate");
    const expenseDateEl = document.getElementById("expenseDate");
    const todayDateEl = document.getElementById("todayDate");
    
    if (incomeDateEl && !incomeDateEl.value) incomeDateEl.value = today;
    if (expenseDateEl && !expenseDateEl.value) expenseDateEl.value = today;
    if (todayDateEl) todayDateEl.textContent = todayDisplay;
}

// --- CATEGORIES API & UI ---
async function loadCategories() {
    try {
        const response = await fetch(`${API_URL}/categories/`);
        if (!response.ok) return;
        const data = await response.json();
        categoriesList = data.categories || [];

        populateCategoryDropdowns();
        renderCategoryListModal();
    } catch (err) {
        console.error("Failed to load categories:", err);
    }
}

function populateCategoryDropdowns() {
    const select = document.getElementById("expenseCategorySelect");
    const editSelect = document.getElementById("editCategorySelect");
    const filterSelect = document.getElementById("categoryFilterSelect");
    
    if (select) {
        select.innerHTML = '<option value="">Select Category...</option>';
        categoriesList.forEach(cat => {
            const opt = document.createElement("option");
            opt.value = cat.id;
            opt.textContent = cat.name;
            select.appendChild(opt);
        });
    }

    if (editSelect) {
        editSelect.innerHTML = '';
        categoriesList.forEach(cat => {
            const opt = document.createElement("option");
            opt.value = cat.id;
            opt.textContent = cat.name;
            editSelect.appendChild(opt);
        });
    }

    if (filterSelect) {
        filterSelect.innerHTML = '<option value="all">All Categories</option>';
        categoriesList.forEach(cat => {
            const opt = document.createElement("option");
            opt.value = cat.name;
            opt.textContent = cat.name;
            filterSelect.appendChild(opt);
        });
        filterSelect.value = currentCategoryFilter;
    }
}

function renderCategoryListModal() {
    const list = document.getElementById("categoryList");
    if (!list) return;
    list.innerHTML = "";

    categoriesList.forEach(cat => {
        const pill = document.createElement("li");
        pill.className = "category-pill";
        pill.innerHTML = `
            <span>${escapeHtml(cat.name)}</span>
            <button onclick="handleDeleteCategory(${cat.id})" title="Delete Category">&times;</button>
        `;
        list.appendChild(pill);
    });
}

function openCategoryModal() {
    document.getElementById("categoryModal").classList.add("open");
}
function closeCategoryModal() {
    document.getElementById("categoryModal").classList.remove("open");
}

async function handleAddCategory(event) {
    event.preventDefault();
    const nameInput = document.getElementById("newCategoryName");
    const name = nameInput.value.trim();

    if (!name) return;

    try {
        const response = await fetch(`${API_URL}/category/add/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name })
        });
        const data = await response.json();

        if (response.ok) {
            nameInput.value = "";
            showToast("Category added successfully!", "success");
            loadCategories();
        } else {
            showToast(data.error || "Failed to add category", "error");
        }
    } catch (err) {
        showToast("Error connecting to server.", "error");
    }
}

async function handleDeleteCategory(categoryId) {
    if (!confirm("Are you sure you want to delete this category?")) return;

    try {
        const response = await fetch(`${API_URL}/category/delete/${categoryId}/`, {
            method: "DELETE"
        });
        if (response.ok) {
            showToast("Category deleted.", "info");
            loadCategories();
        } else {
            const data = await response.json();
            showToast(data.error || "Failed to delete category.", "error");
        }
    } catch (err) {
        showToast("Error connecting to server.", "error");
    }
}

// --- DATA LOADING & METRICS ---
async function loadAllData() {
    try {
        let transactions = [];
        const userParam = currentUser.id ? `user_id=${currentUser.id}` : (currentUser.username ? `username=${encodeURIComponent(currentUser.username)}` : '');
        const queryStr = userParam ? `?${userParam}` : '';
        
        // Fetch Incomes directly
        try {
            const incRes = await fetch(`${API_URL}/income/${queryStr}`);
            if (incRes.ok) {
                const incData = await incRes.json();
                const list = incData.income || [];
                list.forEach(inc => {
                    transactions.push({
                        id: inc.id,
                        type: 'income',
                        title: inc.source,
                        category: 'Income',
                        amount: parseFloat(inc.amount) || 0,
                        date: inc.date,
                        user: inc.user
                    });
                });
            }
        } catch (e) {
            console.error("Error fetching income:", e);
        }

        // Fetch Expenses directly
        try {
            const expRes = await fetch(`${API_URL}/expenses/${queryStr}`);
            if (expRes.ok) {
                const expData = await expRes.json();
                const list = expData.expenses || [];
                list.forEach(exp => {
                    transactions.push({
                        id: exp.id,
                        type: 'expense',
                        title: exp.description || exp.category || 'Expense',
                        category: exp.category || 'General',
                        category_id: exp.category_id,
                        amount: parseFloat(exp.amount) || 0,
                        date: exp.date,
                        user: exp.user
                    });
                });
            }
        } catch (e) {
            console.error("Error fetching expenses:", e);
        }

        // Sort descending by date and id
        transactions.sort((a, b) => (b.date || "").localeCompare(a.date || "") || (b.id - a.id));
        allTransactions = transactions;

        calculateAndDisplayMetrics();
        renderTransactionsTable();
    } catch (err) {
        console.error(err);
        showToast("Failed to sync data from backend.", "error");
    }
}

function calculateAndDisplayMetrics() {
    let totalIncome = 0;
    let totalExpense = 0;

    allTransactions.forEach(item => {
        if (item.type === "income") {
            totalIncome += parseFloat(item.amount) || 0;
        } else if (item.type === "expense") {
            totalExpense += parseFloat(item.amount) || 0;
        }
    });

    const netBalance = totalIncome - totalExpense;

    document.getElementById("totalIncome").textContent = totalIncome.toFixed(2);
    document.getElementById("totalExpense").textContent = totalExpense.toFixed(2);
    document.getElementById("netBalance").textContent = netBalance.toFixed(2);
    document.getElementById("totalRecords").textContent = allTransactions.length;
}

// --- TRANSACTIONS TABLE & FILTERING ---
function filterTransactions(filterType, btn) {
    currentTypeFilter = filterType;
    
    document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
    if (btn) btn.classList.add("active");

    renderTransactionsTable();
}

function filterByCategory(categoryName) {
    currentCategoryFilter = categoryName;

    const banner = document.getElementById("filterBanner");
    const nameLabel = document.getElementById("selectedCategoryName");

    if (categoryName !== "all") {
        banner.classList.remove("hidden");
        nameLabel.textContent = categoryName;
    } else {
        banner.classList.add("hidden");
    }

    renderTransactionsTable();
}

function clearCategoryFilter() {
    currentCategoryFilter = "all";
    const filterSelect = document.getElementById("categoryFilterSelect");
    if (filterSelect) filterSelect.value = "all";

    document.getElementById("filterBanner").classList.add("hidden");
    renderTransactionsTable();
}

function renderTransactionsTable() {
    const tbody = document.getElementById("transactionTableBody");
    tbody.innerHTML = "";

    let filtered = allTransactions;

    // Apply Type Filter
    if (currentTypeFilter === "income") {
        filtered = filtered.filter(t => t.type === "income");
    } else if (currentTypeFilter === "expense") {
        filtered = filtered.filter(t => t.type === "expense");
    }

    // Apply Category Filter
    if (currentCategoryFilter !== "all") {
        filtered = filtered.filter(t => t.category.toLowerCase() === currentCategoryFilter.toLowerCase());
    }

    if (!filtered || filtered.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center">No transaction records match the selected filter.</td>
            </tr>
        `;
        return;
    }

    filtered.forEach(tx => {
        const tr = document.createElement("tr");

        const isIncome = tx.type === "income";
        const badgeClass = isIncome ? "badge-income" : "badge-expense";
        const amountClass = isIncome ? "amount-income" : "amount-expense";
        const prefix = isIncome ? "+ ₹" : "- ₹";

        tr.innerHTML = `
            <td><span class="badge ${badgeClass}">${tx.type}</span></td>
            <td><strong>${escapeHtml(tx.title)}</strong></td>
            <td><span class="category-tag">${escapeHtml(tx.category || 'General')}</span></td>
            <td class="${amountClass}">${prefix}${parseFloat(tx.amount).toFixed(2)}</td>
            <td>${tx.date}</td>
            <td>
                <div class="action-btns">
                    <button class="action-btn" onclick="openEditModal('${tx.type}', ${tx.id})" title="Edit">✏️</button>
                    <button class="action-btn" onclick="handleDeleteTransaction('${tx.type}', ${tx.id})" title="Delete">🗑️</button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function escapeHtml(str) {
    if (!str) return "";
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

// --- ADD INCOME HANDLER ---
async function handleAddIncome(event) {
    event.preventDefault();

    const source = document.getElementById("incomeSource").value.trim();
    const amount = parseFloat(document.getElementById("incomeAmount").value);
    const date = document.getElementById("incomeDate").value;

    try {
        const response = await fetch(`${API_URL}/income/add/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: currentUser.id || undefined,
                username: currentUser.username || undefined,
                source,
                amount,
                date: date || undefined
            })
        });

        const data = await response.json();
        if (response.ok) {
            document.getElementById("incomeForm").reset();
            setTodayDates();
            showToast("Income added successfully!", "success");
            loadAllData();
        } else {
            showToast(data.error || "Failed to add income", "error");
        }
    } catch (err) {
        showToast("Failed to connect to backend server.", "error");
    }
}

// --- ADD EXPENSE HANDLER ---
async function handleAddExpense(event) {
    event.preventDefault();

    const category_id = document.getElementById("expenseCategorySelect").value;
    const description = document.getElementById("expenseDescription").value.trim();
    const amount = parseFloat(document.getElementById("expenseAmount").value);
    const date = document.getElementById("expenseDate").value;

    if (!category_id) {
        showToast("Please select a category.", "error");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/expense/add/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: currentUser.id || undefined,
                username: currentUser.username || undefined,
                category_id: parseInt(category_id),
                description,
                amount,
                date: date || undefined
            })
        });

        const data = await response.json();
        if (response.ok) {
            document.getElementById("expenseForm").reset();
            setTodayDates();
            showToast("Expense added successfully!", "success");
            loadAllData();
        } else {
            showToast(data.error || "Failed to add expense", "error");
        }
    } catch (err) {
        showToast("Failed to connect to backend server.", "error");
    }
}

// --- DELETE HANDLER ---
async function handleDeleteTransaction(type, id) {
    if (!confirm(`Are you sure you want to delete this ${type}?`)) return;

    const endpoint = type === "income" ? `${API_URL}/income/delete/${id}/` : `${API_URL}/expense/delete/${id}/`;

    try {
        const response = await fetch(endpoint, { method: "DELETE" });
        if (response.ok) {
            showToast(`${type.charAt(0).toUpperCase() + type.slice(1)} deleted successfully.`, "info");
            loadAllData();
        } else {
            const data = await response.json();
            showToast(data.error || "Failed to delete item.", "error");
        }
    } catch (err) {
        showToast("Connection error.", "error");
    }
}

// --- EDIT MODAL HANDLERS ---
function openEditModal(type, id) {
    const item = allTransactions.find(t => t.type === type && t.id === id);
    if (!item) return;

    document.getElementById("editItemType").value = type;
    document.getElementById("editItemId").value = id;
    document.getElementById("editModalTitle").textContent = `Edit ${type.toUpperCase()}`;
    
    document.getElementById("editTitle").value = item.title;
    document.getElementById("editAmount").value = item.amount;
    document.getElementById("editDate").value = item.date;

    const catGroup = document.getElementById("editCategoryGroup");
    if (type === "expense") {
        catGroup.classList.remove("hidden");
        document.getElementById("editTitleLabel").textContent = "Description / Title";
        if (item.category_id) {
            document.getElementById("editCategorySelect").value = item.category_id;
        }
    } else {
        catGroup.classList.add("hidden");
        document.getElementById("editTitleLabel").textContent = "Income Source";
    }

    document.getElementById("editModal").classList.add("open");
}

function closeEditModal() {
    document.getElementById("editModal").classList.remove("open");
}

async function handleSaveEdit(event) {
    event.preventDefault();
    const type = document.getElementById("editItemType").value;
    const id = document.getElementById("editItemId").value;

    const amount = parseFloat(document.getElementById("editAmount").value);
    const date = document.getElementById("editDate").value;

    let bodyData = {};
    let endpoint = "";

    if (type === "income") {
        const source = document.getElementById("editTitle").value.trim();
        bodyData = { source, amount, date };
        endpoint = `${API_URL}/income/update/${id}/`;
    } else {
        const description = document.getElementById("editTitle").value.trim();
        const category_id = parseInt(document.getElementById("editCategorySelect").value);
        bodyData = { description, category_id, amount, date };
        endpoint = `${API_URL}/expense/update/${id}/`;
    }

    try {
        const response = await fetch(endpoint, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(bodyData)
        });

        if (response.ok) {
            closeEditModal();
            showToast(`${type.toUpperCase()} updated successfully!`, "success");
            loadAllData();
        } else {
            const data = await response.json();
            showToast(data.error || "Update failed.", "error");
        }
    } catch (err) {
        showToast("Failed to connect to backend server.", "error");
    }
}

// Backwards compatibility alias
function loadIncome() {
    loadAllData();
}
