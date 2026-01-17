let cart = [];
let total = 0;

function addToCart() {
    const select = document.getElementById("productSelect");
    const qty = parseInt(document.getElementById("quantityInput").value);

    if (!qty || qty <= 0) return;

    const name = select.selectedOptions[0].dataset.name;
    const price = parseFloat(select.selectedOptions[0].dataset.price);

    const existing = cart.find(item => item.name === name);

    if (existing) {
        existing.qty += qty;
        existing.itemTotal = existing.qty * existing.price;
    } else {
        cart.push({
            name,
            qty,
            price,
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

    fetch("/prepare_invoice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            customer: {
                name: name,
                phone: customerPhone.value,
                address: customerAddress.value
            },
            cart: cart
        })
    })
    .then(() => {
        window.location.href = "/invoice_preview";
    });
}
