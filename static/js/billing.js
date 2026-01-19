let cart = [];
let total = 0;

const customerName = document.getElementById("customerName");
const customerPhone = document.getElementById("customerPhone");
const customerAddress = document.getElementById("customerAddress");


function addToCart() {
    const select = document.getElementById("productSelect");
    const qty = parseInt(document.getElementById("quantityInput").value);

    if (!qty || qty <= 0) return;

    const option = select.selectedOptions[0];

    const id = option.value;  // <-- IMPORTANT
    const name = option.dataset.name;
    const price = parseFloat(option.dataset.price);

    // const existing = cart.find(item => item.name === name);
    const existing = cart.find(item => item.id === id);


    if (existing) {
        existing.qty += qty;
        existing.itemTotal = existing.qty * existing.price;
    } else {
       cart.push({
    id: id,              // ✅ REQUIRED FOR BACKEND
    name: name,
    qty: qty,
    price: price,
    itemTotal: price * qty
    });

    }

    calculateTotal();
    renderCart();
    flash(`${name} × ${qty} added`);
}
function renderCart() {
    const tbody = document.getElementById("cartTable");
    tbody.innerHTML = "";

    cart.forEach((item, index) => {
        tbody.innerHTML += `
            <tr>
                <td>${item.name}</td>
                <td>
                    <button onclick="changeQty(${index}, -1)">−</button>
                    ${item.qty}
                    <button onclick="changeQty(${index}, 1)">+</button>
                </td>
                <td>Rs ${item.price}</td>
                <td>Rs ${item.qty * item.price}</td>
                <td>
                    <button onclick="removeItem(${index})">✖</button>
                </td>
            </tr>
        `;
    });

    calculateTotal();
}

function changeQty(index, delta) {
    cart[index].qty += delta;

    if (cart[index].qty <= 0) {
        cart.splice(index, 1);
    } else {
        cart[index].itemTotal = cart[index].qty * cart[index].price;
    }

    renderCart();
}

function removeItem(index) {
    cart.splice(index, 1);
    renderCart();
}


function calculateTotal() {
    total = cart.reduce((sum, item) => sum + (item.qty * item.price), 0);
    document.getElementById("grandTotal").innerText = `Rs ${total}`;
}

function showToast(msg, type="success") {
    const toast = document.getElementById("flash-toast");
    toast.innerText = msg;
    toast.style.background = type === "error" ? "#dc2626" : "#16a34a";
    toast.style.display = "block";

    setTimeout(() => {
        toast.style.display = "none";
    }, 2200);
}

function printBill() {
    window.print();
}

function downloadBill() {
    alert("PDF download can be connected later via backend");
}

// function confirmInvoice() {

//     if (cart.length === 0) {
//         alert("Bill is empty. Add at least one product.");
//         return;
//     }

//     const name = customerName.value.trim();
//     const phone = customerPhone.value.trim();

//     if (!name || !phone) {
//         alert("Customer name and phone are required.");
//         return;
//     }

//     fetch("/prepare_invoice", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//             customer: {
//                 name: name,
//                 phone: phone,
//                 address: customerAddress.value
//             },
//             cart: cart
//         })
//     })
//     .then(res => {
//         if (!res.ok) throw new Error("Prepare failed");
//         return fetch("/confirm_invoice", { method: "POST" });
//     })
//     .then(res => {
//         if (!res.ok) throw new Error("Save failed");
//         window.location.href = "/invoice_preview";
//     })
//     .then(() => {
//         setTimeout(() => window.print(), 500);
//     })
//     .catch(err => {
//         alert("Invoice failed");
//         console.error(err);
//     });
// }

function confirmInvoice() {

    if (cart.length === 0) {
        alert("Bill is empty. Add at least one product.");
        return;
    }

    const name = customerName.value.trim();
    const phone = customerPhone.value.trim();

    if (!name || !phone) {
        alert("Customer name and phone are required.");
        return;
    }

    // Only make ONE fetch call to prepare the invoice data
    fetch("/prepare_invoice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            customer: {
                name: name,
                phone: phone,
                address: customerAddress.value
            },
            cart: cart
        })
    })
    .then(res => {
        if (!res.ok) throw new Error("Prepare failed");
        // Immediately redirect the user to the invoice preview page
        // The browser will send the newly set session cookie automatically
        window.location.href = "/invoice_preview";
    })
    .catch(err => {
        // This catch block handles the error shown in your image
        alert("Invoice failed: " + err.message);
        console.error(err);
    });
}

function printQuotation() {

    if (cart.length === 0) {
        alert("Bill is empty. Add at least one product.");
        return;
    }

    const name = customerName.value.trim();
    const phone = customerPhone.value.trim();

    if (!name || !phone) {
        alert("Customer name and phone are required.");
        return;
    }

    fetch("/prepare_invoice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            customer: {
                name: name,
                phone: phone,
                address: customerAddress.value
            },
            cart: cart
        })
    })
    .then(res => {
        if (!res.ok) throw new Error("Failed");
        window.location.href = "/invoice_preview";
    })
    .then(() => {
        setTimeout(() => window.print(), 500);
    })
    .catch(err => {
        alert("Quotation failed");
        console.error(err);
    });
}
