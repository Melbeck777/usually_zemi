<template>
    <footer>
        <p>Create Summary & Index</p>
    </footer>
</template>

<style>
footer {
    background-color: rgb(25, 215, 41);
    color: white;
    padding: 0 20px;
    margin-top: 160px;
    font-size: 20px;
    width: 100%;
}
@media (min-width: 768px) {
    footer {
        position: fixed;
        bottom: 0;
        padding: 0;
        height: 50px;
        display: gird;
        grid-template-columns: 1fr 700px 1fr;
        grid-template-rows: 1fr;
    }
    footer > * {
        grid-column: 1;
        grid-row: 1;
    }
    p {
        justify-self: start;
        align-self: center;
    }
}
@media(min-width: 1024px) {
    footer {
        grid-template-columns: 1fr 980px 1fr;
    }
}
</style>