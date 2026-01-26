/**
 * Social sharing utilities for BhashaMitra
 * Supports WhatsApp, SMS, Email, and Copy Link
 */

export interface ShareData {
  title: string;
  text: string;
  url: string;
}

/**
 * Check if Web Share API is available (mobile devices)
 */
export function canShare(): boolean {
  if (typeof window === 'undefined') return false;
  return 'share' in navigator || 'canShare' in navigator;
}

/**
 * Native share using Web Share API
 */
export async function nativeShare(data: ShareData): Promise<boolean> {
  if (!canShare()) return false;
  
  try {
    if ('share' in navigator) {
      await navigator.share(data);
      return true;
    }
    return false;
  } catch (error) {
    console.error('Share failed:', error);
    return false;
  }
}

/**
 * Share to WhatsApp - opens WhatsApp app with pre-filled message
 */
export function shareToWhatsApp(message: string, url?: string): void {
  const fullMessage = url ? `${message}\n\n${url}` : message;
  const encodedMessage = encodeURIComponent(fullMessage);
  window.open(`https://wa.me/?text=${encodedMessage}`, '_blank');
}

/**
 * Share via SMS - opens default SMS app
 */
export function shareViaSMS(phoneNumber: string, message: string, url?: string): void {
  const fullMessage = url ? `${message} ${url}` : message;
  const encodedMessage = encodeURIComponent(fullMessage);
  window.location.href = `sms:${phoneNumber}?body=${encodedMessage}`;
}

/**
 * Share via Email
 */
export function shareViaEmail(email: string, subject: string, body: string): void {
  const encodedSubject = encodeURIComponent(subject);
  const encodedBody = encodeURIComponent(body);
  window.location.href = `mailto:${email}?subject=${encodedSubject}&body=${encodedBody}`;
}

/**
 * Copy URL to clipboard
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    console.error('Copy failed:', error);
    return false;
  }
}

/**
 * Generate family invite message
 */
export function generateFamilyInviteMessage(familyName: string, inviteCode: string, inviterName?: string): string {
  const inviter = inviterName ? `${inviterName} has` : 'You have';
  return `${inviter} invited you to join the "${familyName}" family on PeppiAcademy!\n\nUse code: ${inviteCode}`;
}

/**
 * Generate deep link URL for family joining
 */
export function getFamilyJoinUrl(inviteCode: string, baseUrl?: string): string {
  const base = baseUrl || (typeof window !== 'undefined' ? window.location.origin : 'https://bhashamitra.com');
  return `${base}/join/${inviteCode}`;
}

/**
 * Share family invite via multiple channels
 */
export async function shareFamilyInvite(
  familyName: string,
  inviteCode: string,
  channel: 'whatsapp' | 'sms' | 'copy',
  inviterName?: string
): Promise<{ success: boolean; message?: string }> {
  const message = generateFamilyInviteMessage(familyName, inviteCode, inviterName);
  const url = getFamilyJoinUrl(inviteCode);
  
  switch (channel) {
    case 'whatsapp':
      shareToWhatsApp(message, url);
      return { success: true };
    
    case 'copy':
      const fullText = `${message}\n\n${url}`;
      const copied = await copyToClipboard(fullText);
      return { 
        success: copied, 
        message: copied ? 'Link copied to clipboard!' : 'Failed to copy' 
      };
    
    case 'sms':
      shareViaSMS('', message, url);
      return { success: true };
    
    default:
      return { success: false, message: 'Unknown sharing method' };
  }
}

/**
 * Track sharing event for analytics
 */
export function trackShareEvent(method: string, contentType: string): void {
  console.log(`Shared ${contentType} via ${method}`);
}
