from customfs import InMemoryFS

fs = InMemoryFS()

fs.create("file1.txt")
fs.create("file2.txt")
fs.link("file1.txt", "alias1.txt")

fd1 = fs.open("file1.txt")
fd2 = fs.open("file2.txt")

fs.write(fd1, b"This is content for file1")
fs.write(fd2, b"This is content for file2")
fs.unlink("alias1.txt")

print(fs.ls())  # Output: ["file1.txt", "file2.txt"]

data = fs.read(fd1, 10)
print(data.decode())  # Output: "This is co"



fs.close(fd1)

fs.write(fd2, b"\nAppended content")
print(fs.read(fd2, 20).decode())  # Output: "Appended content"
fs.truncate("file2.txt", 10)
fs.close(fd2)