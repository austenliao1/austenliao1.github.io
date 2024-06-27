document.addEventListener('DOMContentLoaded', () => {
    const publications = [
        { title: "Publication 1", link: "https://example.com/publication1" },
        { title: "Publication 2", link: "https://example.com/publication2" },
        { title: "Publication 3", link: "https://example.com/publication3" }
    ];

    const publicationList = document.getElementById('publication-list');
    publications.forEach(pub => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = pub.link;
        a.textContent = pub.title;
        a.target = "_blank";
        li.appendChild(a);
        publicationList.appendChild(li);
    });

    document.getElementById('contact-form').addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Form submitted!');
        // Here you can add the code to handle form submission, e.g., sending the data to your server
    });
});
