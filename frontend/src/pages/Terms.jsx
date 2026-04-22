import Layout from '../components/layout'

function Terms() {
  return (
    <Layout>
      <div style={{ padding: '40px 20px', maxWidth: '900px' }}>
        
        <h1
          style={{
            fontFamily: "'Sora', sans-serif",
            fontWeight: 700,
            color: '#1a6b7a',
            letterSpacing: '1px',
            marginBottom: '8px'
          }}
        >
          Terms and Conditions
        </h1>

        <p style={{ color: '#666', marginBottom: '24px' }}>
          Last updated: 21/04/2026
        </p>

        <h2>1. Introduction</h2>
        <p>
          These Terms and Conditions govern your use of Atlas, a cloud-based API service
          for generating and managing UBL 2.1 Despatch Advice documents. By using Atlas,
          you agree to these terms.
        </p>

        <h2 style={{ marginTop: '20px' }}>2. Use of Service</h2>
        <p>
          Atlas provides automated generation, storage, and management of despatch advice
          documents. You agree to use the service only for lawful business purposes and
          in compliance with applicable regulations.
        </p>

        <h2 style={{ marginTop: '20px' }}>3. User Accounts</h2>
        <p>
          You are responsible for maintaining the confidentiality of your account and
          session token. Any activity performed under your account is your responsibility.
        </p>

        <h2 style={{ marginTop: '20px' }}>4. Data Accuracy</h2>
        <p>
          Atlas generates documents based on the data you provide. We do not guarantee
          the accuracy of generated documents if incorrect or incomplete data is submitted.
        </p>

        <h2 style={{ marginTop: '20px' }}>5. Availability</h2>
        <p>
          We aim to provide reliable service but do not guarantee uninterrupted availability.
          Atlas is provided on an "as is" basis.
        </p>

        <h2 style={{ marginTop: '20px' }}>6. Limitation of Liability</h2>
        <p>
          Atlas is not liable for any indirect, incidental, or consequential damages,
          including loss of business or data arising from use of the service.
        </p>

        <h2 style={{ marginTop: '20px' }}>7. Termination</h2>
        <p>
          We reserve the right to suspend or terminate accounts that violate these terms.
        </p>

        <h2 style={{ marginTop: '20px' }}>8. Changes to Terms</h2>
        <p>
          These terms may be updated at any time. Continued use of Atlas constitutes
          acceptance of the updated terms.
        </p>

        <h2 style={{ marginTop: '20px' }}>9. Contact</h2>
        <p>
          For questions regarding these terms, contact us at atlasenquires@gmail.com.
        </p>

      </div>
    </Layout>
  )
}

export default Terms