import Layout from '../components/layout'

function Privacy() {
  return (
    <Layout>
      <div style={{ padding: '40px 20px', maxWidth: '900px' }}>
        
        {/* Title */}
        <h1
          style={{
            fontFamily: "'Sora', sans-serif",
            fontWeight: 700,
            color: '#1a6b7a',
            letterSpacing: '1px',
            marginBottom: '8px'
          }}
        >
          Privacy Policy
        </h1>

        <p style={{ color: '#666', marginBottom: '24px' }}>
          Last updated: 21/04/2026
        </p>

        <h2>1. Information We Collect</h2>
        <p>
          We collect information such as your name, email address, and any despatch
          documents submitted through Atlas.
        </p>

        <h2 style={{ marginTop: '20px' }}>2. How We Use Information</h2>
        <p>
          Your data is used to provide and improve the Atlas service, including
          generating, storing, and retrieving despatch advice documents.
        </p>

        <h2 style={{ marginTop: '20px' }}>3. Data Storage</h2>
        <p>
          Data is securely stored using cloud infrastructure with appropriate
          safeguards in place.
        </p>

        <h2 style={{ marginTop: '20px' }}>4. Security</h2>
        <p>
          We use authentication tokens and secure systems to protect your data.
          However, no system can be completely secure.
        </p>

        <h2 style={{ marginTop: '20px' }}>5. Contact</h2>
        <p>
          For privacy-related inquiries, contact us at yatlaseqnuires@gmail.com.
        </p>

      </div>
    </Layout>
  )
}

export default Privacy