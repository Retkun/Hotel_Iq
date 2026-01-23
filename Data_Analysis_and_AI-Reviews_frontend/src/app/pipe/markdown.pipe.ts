import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'markdown',
  standalone: true
})
export class MarkdownPipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}

  transform(value: string): SafeHtml {
    if (!value) {
      return '';
    }

    // Replace **text** with <strong>text</strong> for bold
    let formattedText = value.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Replace *text* or _text_ with <em>text</em> for italic
    formattedText = formattedText.replace(/(?:\*|_)(.*?)(?:\*|_)/g, '<em>$1</em>');

    // Ensure newlines are preserved as <br>
    formattedText = formattedText.replace(/\n/g, '<br>');

    // Sanitize the HTML to prevent XSS attacks
    return this.sanitizer.bypassSecurityTrustHtml(formattedText);
  }
}