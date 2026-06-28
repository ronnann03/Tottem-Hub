export default function PublicLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-white">
      {/* TODO: Navbar público */}
      <main>{children}</main>
      {/* TODO: Footer público */}
    </div>
  );
}
